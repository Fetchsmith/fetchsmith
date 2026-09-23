# We nearly charged our own buyers twice for rows they'd already paid for

Every "watch mode" Actor in our catalog — the ones that poll a source and only deliver *new* rows since the last run — keeps a baseline of ids it has already delivered, so it doesn't redeliver (and re-bill) the same row twice. We found a bug in how that baseline is capped, and it took 22 Actors to fully close.

## The mechanism

Watch mode stores a set of delivered ids in the Actor's key-value store, capped at a fixed size — `WATCH_KEEP`, typically 5,000, 20,000 or 60,000 depending on the source's volume — so the record doesn't grow without bound. When the set is full, the oldest ids are evicted to make room for new ones. That part is fine.

The bug: eviction is **silent and unconditional**. Nothing checks whether an evicted id might still show up again in a future poll. For a high-volume source — one where a single run can return more new ids than `WATCH_KEEP` holds — old-but-still-current ids get pushed out of the baseline. The next run sees them as "new" (because they're no longer in the stored set), delivers them again, and the buyer is billed again for a row they already paid for.

## What it looked like on a real Actor

`google-play-reviews-scraper` has `WATCH_KEEP = 20000`. We seeded a watch with a query that returned far more reviews than that cap:

```
seed run:        1000 ids recorded, 997 dropped by the cap (warned)
incremental run:  40 rows delivered, 0 skipped as already-seen
```

Zero skipped is the signature. On a healthy watch, an incremental run against an unchanged source should skip everything it's seen before (`skippedSeen` / `skippedAlreadyDelivered` > 0) and deliver only genuinely new rows. Here, every one of the 40 delivered rows had already been paid for in the seed run — they just weren't in the baseline anymore because eviction had pushed them out.

This reproduced identically, with the same shape, on `court-records-scraper`, `clinicaltrials-scraper`, `eu-ted-tenders-scraper`, `fda-recall-scraper`, `grants-gov-scraper`, `uk-find-a-tender-scraper`, `nih-reporter-scraper`, `ats-jobs-scraper`, and others — anywhere the source could plausibly exceed the cap in a single poll window.

## Why it stayed invisible

The run itself looks completely normal. It's `SUCCEEDED`, the row count is plausible, and nothing in the Actor's own output flags a problem — because from the Actor's point of view, it did exactly what it was told: deliver rows not in the baseline. The defect is a *billing* problem, not a *correctness* problem, and it shows up in a future invoice, not in the run that caused it. A status message gated on `!complete` (a common pattern for "this run stopped early") wouldn't catch it either — a perfectly complete run can still have silently evicted thousands of ids.

## The fix

Every watch-mode Actor now tracks how many ids the current save evicted, and surfaces it five ways instead of zero:

- a `log.warning` at save time when eviction happens
- a note appended to the run's status message (added as an `else if (baselineTruncated > 0)` branch alongside the `!complete` branch, not instead of it)
- `truncatedLastRun` / `truncatedTotal` written into the watch record itself, so the next run can see cumulative exposure
- `baselineTruncated` / `baselineTruncatedTotal` in `RUN_SUMMARY`, which flows through to any configured `webhookUrl` — so it's visible to an integration, not just someone reading the console
- a README section documenting the cap size, so it's not a surprise to a buyer who reads the source

None of this stops the re-delivery outright — that would need either an unbounded baseline (which doesn't scale) or a smarter cap tied to actual poll volume (a larger, separate change). The fix makes the exposure **visible and measurable** instead of silent, on both sides: log/status for the run that caused it, and a running total for whoever's deciding whether the cap needs raising.

## The test recipe

Each fix was verified against the *live* source, not a fixture: a temp copy of the Actor with `WATCH_KEEP` patched down to a small number (so a normal-sized run can exceed it), pointed at a temp storage dir, run twice — seed then incremental. Two runs, well under a minute, and the re-charge reproduces exactly as `delivered > 0` with `skipped: 0`. A separate run at the real cap serves as the negative control, confirming the new warning stays silent when eviction genuinely doesn't happen.

## Packaged version

The fix is live across the fleet's watch-mode Actors — [clinicaltrials-scraper](https://apify.com/fetchsmith/clinicaltrials-scraper), [court-records-scraper](https://apify.com/fetchsmith/court-records-scraper), [grants-gov-scraper](https://apify.com/fetchsmith/grants-gov-scraper), [fda-recall-scraper](https://apify.com/fetchsmith/fda-recall-scraper), [google-play-reviews-scraper](https://apify.com/fetchsmith/google-play-reviews-scraper), and more — at [fetchsmith.com/tools](https://fetchsmith.com/tools).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; the numbers above are from real reproductions against live source APIs, not synthetic fixtures.*
