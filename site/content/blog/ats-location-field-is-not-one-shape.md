---
title: "Location is not one field either: normalizing ten ATS job-board APIs down to city/region/country"
description: Three of ten applicant-tracking systems hand back structured geography, three hand back one free-text string a human typed, and Workday's list payload gives you neither — it takes a second per-job call to resolve, and until 0.1.39 that call ran too late to help its own filter.
date: 2026-10-20
tags: webscraping, api, jobs, hiring
tool: ats-jobs-scraper
---

If `employmentType` is [three different kinds of field wearing one name](/blog/ats-employment-type-is-not-one-vocabulary), location is worse — because on four of our ten platforms it isn't a field at all. It's a sentence someone typed into a text box, and the sentence doesn't agree with itself from one posting to the next on the same board.

We normalize ten applicant-tracking systems into one schema in [ats-jobs-scraper](/go/ats-jobs-scraper), which means deciding, per platform, how `city`/`region`/`country` get filled — and when to leave them `null` instead of guessing. The short answer: three platforms already hand back structured geography, one hands back structured geography with a trap field disguised as a region, and the rest are free text that has to be parsed against a vocabulary that will never cover every string a human can type.

## Structured, free text, or nothing

**Structured, pass-through.** Ashby, Lever, Recruitee, SmartRecruiters, Workable and Breezy all publish real `city`/`state`/`country`-shaped fields. Nothing to parse — the board already did the work. Re-verified live today: Breezy's two real boards (`the-san-francisco-standard`, `breezy.breezy.hr`'s demo tenant) still fill `country`, `region` and `city` on all 9 of their combined postings, no `null`s.

**Structured, with one trap.** Teamtailor's board feed embeds a full schema.org `JobPosting`, so `city` comes from `jobLocation[].address.addressLocality` — also structured, also a pass-through. But the field that looks like the obvious source for our `region` column, `addressRegion`, is not usable: re-checked live today across `oatly` (19 postings), `schibsted` (32), `doconomy` (1) and `career.teamtailor.com` (15) — 67 postings total — `addressRegion` is missing outright on 33 of them (schibsted's 32 and doconomy's 1, i.e. every posting on two of the four boards), and on the other 34 it's either a continent (`"North America"`, `"Oceania"`, `"Europe"`) or a repeat of the country (`"United States"`, `"Sweden"`). It is never a real state or province. We leave `region: null` for Teamtailor rather than ship a continent mislabeled as one.

**Free text, parsed against a vocabulary.** Greenhouse's `location.name` and Personio's `office` are both a single hand-typed string, and we run the same normalizer — `parseLocation()` — on both. Workday's list payload is a third flavor of the same problem: one string per posting, formatted differently by every tenant (`"US, CA, Santa Clara"`, `"France - Paris"`, `"Canada, Toronto"`), fed through the identical normalizer.

**Nothing, until a second call.** Workday's job-listing payload carries that one free-text string and nothing else — no separate country or city field exists on the list endpoint at all. The per-job detail call adds one structured field, which is where the real fill-rate jump below comes from.

## Fill rates, measured live

| ATS | Source shape | Sample | `country` fills | `city` fills | `region` fills |
|---|---|---|---|---|---|
| Ashby / Lever / Recruitee / SmartRecruiters / Workable | structured, pass-through | — | 100% | 100% | 100%* |
| Breezy | structured, pass-through | 9 postings, 2 boards | 100% | 100% | 100% |
| Teamtailor | structured `city`; `region` deliberately dropped | 67 postings, 4 boards | 100% | 100% | **0%** (by design) |
| Greenhouse | free text, parsed | 177 postings, `airbnb` | ~96%** | ~68%** | ~51%** |
| Personio | free text, parsed | 10 postings, `ottonova` | high | high | low (German place names) |
| Workday, list only | one opaque string | 800 postings (`nvidia`/`salesforce`/`adobe`/`okgov`) | 35% | 22% | 14% |
| Workday, + detail call | + one structured field | same 800 | **100%** | — | — |

\* structured fields fill whenever the board itself populates them; not independently re-measured this cycle. \*\* re-measured live today on a fresh 177-posting pull (airbnb's board has grown from the 1,914-posting, 5-company sample behind the original 95/67/50% figures); directionally consistent, cited here as the single-board spot-check, not a replacement for the full sample.

## Greenhouse: the trap isn't a bug, it's a tempting fallback we refuse to take

Greenhouse also publishes a per-posting `offices[]` array with a cleaner-looking `name` field, and the obvious move when `location.name` doesn't parse is to fall back to it. We measured why that's wrong once (1,914 live postings across `airbnb`, `databricks`, `figma`, `stripe`, `discord`) and it's stayed wrong: `offices[]` routinely **contradicts** the posting it's attached to. A `databricks` posting located in `"Finland"` carries a `"Denmark"` office. A `"Nevada"` posting carries a `"Remote - Texas"` office. Trusting the office array to fill a gap on one board invents a wrong answer, not a missing one — so we don't use it, ever, even when `location.name` fails to parse.

The California example is the clearest illustration of why the parser exists at all rather than a plain substring check on the raw text. Re-verified live today against the real `airbnb` board (177 postings, was 163 at last measurement — boards grow): `locationKeyword: "California"` returns **16** rows. Only **2** of those say "California" anywhere in the board's own location text — the rest are `"San Francisco, CA"`, `"Los Angeles, CA"` and similar city strings our vocabulary resolves to the state. A buyer filtering on the literal word would miss 14 of 16 genuinely-matching postings.

## Workday: the field exists, just not where — or when — you'd expect

Workday's list payload hands back `locationsText`, a free string, and nothing structured next to it. Running the same `parseLocation()` normalizer against that text (rather than leaving Workday at `null` forever, which is what the Actor did before this existed) fills `country` on 35%, `city` on 22%, `region` on 14% of 800 live postings sampled across `nvidia`, `salesforce`, `adobe` and `okgov`. Turning on `includeDescriptions` adds a second, per-job call that includes Workday's own structured `country.descriptor` field, and `country` jumps to **100%** — its spelling, `"United States of America"`, gets normalized to `"United States"` so it groups with every other platform's rows instead of forming its own bucket. That second call is also the only way to resolve postings the list page shows only as `"3 Locations"`, which accounts for most of the extra `city`/`region` fill.

The practical effect, measured on the same 800 postings: `locationKeyword: "United States"` matched **0** before the detail-call resolution existed and **89** after.

**That number was still wrong for one board shape, and the fix shipped in 0.1.39.** `okgov`, a county-government tenant, writes its list text as county names only — `"Muskogee County"`, `"Craig County"` — with no country or state anywhere in the string. The filter used to check `locationKeyword` against the un-resolved list text *before* the detail call that would have filled in `country`, so every one of those postings got dropped as a non-match even though the resolved value would have passed. Re-measured live on `okgov` after the fix: `locationKeyword: "United States"` went from **0 of 10** to **10 of 10**. A later, larger re-check on the full visible board (60 of 60 postings, not the earlier 10-row sample) held: **60 of 60** matched, and the earlier proof generalized rather than being a sample-size fluke.

## What we refuse to guess

Across every platform, anything the vocabulary doesn't recognize stays `null`. That specifically means: multi-country zones (`"EMEA"`, `"APAC"`), placeholders (`"N/A"`, the literal word `"Remote"`), internal office abbreviations (`"SF"`, `"CHI"`, `"ATL"`), and the single token `"Georgia"` — equally the US state and the country, so we carry neither. Real German place names outside our gazetteer (`"Singen am Hohentwiel"`, the field-sales label `"Außendienst Köln"`) come back `null` on Personio rather than a bad guess. Where a posting lists several places, the fields describe the first one and the rest stay in `secondaryLocations` rather than getting silently dropped.

## Practical rules

- **Structured fields don't need a parser; free text always needs a vocabulary, and a vocabulary is always incomplete.** Budget for `null`s — a wrong country is a worse answer than a missing one.
- **Don't fall back to a "cleaner-looking" adjacent field without measuring it first.** Greenhouse's `offices[]` looks like a gap-filler and is actually a source of contradictions.
- **A field that looks like a region (`addressRegion`) is not always usable as one.** Teamtailor's version is a continent or a country repeat — check what's actually in it before you map it.
- **Order of operations matters as much as which fields you read.** Workday's county-board bug wasn't a missing field, it was a filter running before the call that resolves it.

[ats-jobs-scraper](/go/ats-jobs-scraper) normalizes all ten platforms' location data into the same `city`/`region`/`country`/`secondaryLocations` shape, with `locationKeyword`/`locationExcludeKeyword` matching against the raw text and every normalized field at once. Pay per job posting returned, no start fee, no browser needed for any of the ten.

## Related reading

- ["full-time" is not a filter: employmentType across ten ATS job-board APIs](/blog/ats-employment-type-is-not-one-vocabulary)
- [Six ATS job-board JSON APIs, six different ideas of what a job posting is](/blog/ats-job-board-json-apis-six-shapes)
- [Teamtailor, Personio and Breezy — three more ATS job-board APIs, three more shapes](/blog/teamtailor-personio-breezy-job-board-apis)
- [Workday's public career-site API has no auth, a hard page-size cap, and no department field](/blog/workday-career-site-json-api)

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; the Greenhouse, Teamtailor and Personio figures quoted above as re-checked were fetched from the live boards while writing this post.*
