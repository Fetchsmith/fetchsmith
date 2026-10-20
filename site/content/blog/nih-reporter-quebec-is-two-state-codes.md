---
title: NIH RePORTER codes Quebec as two different states, and asking for the valid one returns 2 institutions out of 21
description: org_states QC and PQ are both live codes in NIH RePORTER today, holding disjoint sets of awards. QC is effectively McGill plus one Montreal institute; PQ holds the other 19 organizations and is still being issued in FY2026. A valid-value check cannot catch this — live-measured counts, per-institution.
date: 2026-10-20
tags: webscraping, api, opendata, nih, grants
tool: nih-reporter-scraper
---

Most filter bugs announce themselves. You send a misspelled field name and get the whole index back ([NIH RePORTER does exactly that](/blog/nih-reporter-grants-json-api)); you send a nonexistent activity code and get zero rows. Both are detectable: one returns absurdly too much, the other returns nothing, and an Actor can validate the value against a known vocabulary before it ever sends the request.

There is a third shape that defeats validation entirely. The code you sent is real. The result is non-empty. The numbers look plausible. And you are still missing most of what you asked for — because the vocabulary contains *two* live codes for one real-world place, and nothing in the response says so.

## Both codes are real, and they do not overlap

NIH RePORTER's `org_states` criteria accepts two-letter codes. Quebec has two of them: the current postal abbreviation `QC`, and `PQ` — "Province de Québec", a form Canada Post retired decades ago. Measured live, 2026-10-20, against the public search endpoint:

```json
POST https://api.reporter.nih.gov/v2/projects/search
{"criteria": {"org_states": ["QC"]}, "limit": 1}
```
```json
{"meta": {"total": 244}}
```
```json
{"criteria": {"org_states": ["PQ"]}, "limit": 1}
```
```json
{"meta": {"total": 605}}
```

849 awards across the two. Pulling every row from both and intersecting on `appl_id` gives **zero overlap** — these are not two views of one set, they are a clean partition of Quebec into two codes. So `orgStates: ["QC"]` is a valid filter returning 244 real, correctly-matched awards, and silently omitting 605 others.

That part was already in [`nih-reporter-scraper`](/tools/nih-reporter-scraper)'s README. Re-measuring it this month to check it hadn't drifted turned up something the README had wrong.

## `QC` is not "the newer half of Quebec". It is two institutions.

Group both code's awards by organization name and the asymmetry is not a near-even split:

| | awards | distinct organizations | fiscal years |
|---|---|---|---|
| `QC` | 244 | **2** | 1995–2025 |
| `PQ` | 605 | **21** | 1987–2026 |

Every award ever coded `QC` belongs to one of two organizations:

```
 191  MCGILL UNIVERSITY                        FY2008-2025
  53  CLINICAL RESEARCH INSTITUTE OF MONTREAL  FY1995-2016
```

Université de Montréal, Laval, Concordia, UQAM, Montreal Heart Institute, Sainte-Justine, the Douglas, the Jewish General, École Polytechnique, INRS, McGill University Health Centre — **all 19 of them have never had a single award coded `QC`.** They are `PQ`, and they still are.

So the practical rule is not "ask for both to be thorough". It is: ask for `QC` alone and you have queried McGill and one Montreal institute, not a province. That is 29% of Quebec's awards and 2/21 of its research organizations, which is the opposite of the "roughly half" our own README claimed before this measurement.

## `PQ` is not a legacy code, either

The tempting conclusion is that `PQ` is a historical artifact: old awards got the old code, new ones get the new one, and a query filtered to recent years is safe with `QC` alone. It isn't. Restricting both pulls to FY2020 and later:

```
QC  FY2020+ : 47 awards   1 organization   (McGill University)
PQ  FY2020+ : 62 awards   8 organizations  (CHU de Montréal 13, Sainte-Justine 12,
                                            Montreal Heart Institute 9, Douglas 8,
                                            Université de Montréal 7, MUHC 6,
                                            Laval 4, UQAM 3)
```

`PQ` carries *more* recent awards than `QC` does, from eight times as many institutions, with records reaching FY2026. Both codes are actively being written today.

## What the split actually tracks

McGill is the one organization that appears under both names, and its awards divide with no overlapping year at all:

```
MCGILL UNIVERSITY  under PQ:  201 awards,  FY1992-2007
MCGILL UNIVERSITY  under QC:  191 awards,  FY2008-2025
```

A clean cutover at FY2008 — and every other Quebec institution went through FY2008 without one. That rules out a province-wide or NIH-wide migration; if RePORTER had re-coded Quebec in 2008, Laval and Université de Montréal would have moved too, and they didn't (Laval ran `PQ` to FY2021, Université de Montréal to FY2024).

What's left is the mundane explanation: the state code travels with the grantee's own institutional profile, so it changes when *that organization* updates its registration, and never otherwise. One institution modernized its address in 2008; the others kept filing the form the way they always had. There is no cutover date to filter around, no "use QC after year N" rule, and no reason to expect `PQ` to stop appearing.

## Why a valid-value check can't save you

[`nih-reporter-scraper`](/tools/nih-reporter-scraper) validates `orgStates` against the real 70-code closed set RePORTER accepts (50 states, DC, 5 territories, 3 Compact-of-Free-Association states, UM, and 10 Canadian provinces — found by brute-forcing all 676 two-letter combinations against the live API, because NIH publishes no reference endpoint for this vocabulary). That check catches `UK`, catches `US`, catches typos.

It cannot catch this one, and no validity check could: `QC` *is* in the closed set. `PQ` *is* in the closed set. Both return real rows. The error isn't in the value you sent — it's that the vocabulary has two entries where the world has one province, and a per-value check has no way to know that two codes are synonyms when the data treats them as unrelated.

The only defense is a rule about *pairs*, which is what the Actor does instead: ask for one of `QC`/`PQ` without the other and the run logs a warning naming the code you're missing. The value still goes through unchanged — it's a legitimate query, and you may well want McGill specifically — but you find out before you build a dashboard on 29% of a province.

**For all of Quebec, pass `orgStates: ["QC","PQ"]`.**

## The general shape

This is worth checking in any closed-vocabulary filter over a long-lived administrative dataset, not just this one:

- **Synonym pairs survive in reference data far longer than in the real world.** `PQ` has not been a current Canadian postal abbreviation for decades and is still the majority code for Quebec in a federal research database being written to in FY2026.
- **A split vocabulary is invisible from one query.** Nothing in a `QC` response hints that `PQ` exists; the `meta.total` is a confident number for a question you didn't mean to ask.
- **"Recent data only" does not make it safe.** We checked, and the legacy code is the *more* active one in the last six years.
- **Checking the distinct-entity count, not just the row count, is what exposes it.** 244 rows looked like a plausible Quebec; 2 organizations did not. If you only ever compare totals, a vocabulary split reads as a small region.

## Packaged version

[nih-reporter-scraper on Apify](/go/nih-reporter-scraper) validates every `orgStates` value against the measured 70-code set, warns when you ask for `QC` or `PQ` without its twin, and auto-chunks past the API's 15,000-row offset wall so a province-wide query is traversable in the first place. Every figure above came from the public RePORTER endpoint while writing this post.

See [the first guide](/blog/nih-reporter-grants-json-api) for the 15,000-row wall and the unrecognised-criteria-key trap, [the shared-search guide](/blog/nih-reporter-search-id-vs-criteria) for pasting a reporter.nih.gov link straight into the API, and [eight government JSON APIs that need no key](/blog/free-government-data-json-apis-no-key) for how this API's silent-failure shape compares to the rest.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every JSON snippet and count above comes from a live request made while writing this post, not from documentation.*
