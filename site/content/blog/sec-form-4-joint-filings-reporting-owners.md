---
title: One Form 4 can name ten reporting owners — and EDGAR's daily index lists the filing once per owner
description: A joint Form 4 (two or more reporting owners on one filing) breaks two things at once: the EDGAR daily index counts the filing once per CIK, so a naive row count overstates the day's filings by 1.4x–2.0x, and any role filter that reads only the first reporting owner silently drops rows that genuinely match. Measured over three consecutive trading days — 1,038 Form 4s, 38 joint — the joint rate swings from 1.3% to 7.4% day to day, so it cannot be quoted from one sample.
date: 2026-10-19
tags: webscraping, sec, edgar, finance, dataquality
tool: sec-insider-trades-scraper
---

A Form 4 is usually one insider reporting their own trade. Sometimes it isn't: SEC rules let two or more **reporting owners** file a single Form 4 together — a fund and its general partner, a CEO and the holding company they control, five Blackstone entities in one control chain. The filing carries one `<reportingOwner>` block per owner, and both EDGAR's index and most tooling flatten that structure in ways that quietly change your numbers.

[sec-insider-trades-scraper](/go/sec-insider-trades-scraper) parses the raw ownership XML rather than a pre-flattened feed, so it has to make a decision about every one of those blocks. Here is what three days of live measurement against EDGAR's public daily index says about that decision.

## Gotcha 1: a day's index has far more Form 4 rows than Form 4 filings

EDGAR's daily form index (`https://www.sec.gov/Archives/edgar/daily-index/2026/QTR4/form.YYYYMMDD.idx`) lists a filing once **per CIK attached to it** — the issuer *and* every reporting owner. A single-owner Form 4 therefore occupies **two** rows, not one, and a joint filing occupies three or more. Counting rows and calling the result "Form 4s filed today" overstates the day by roughly the average owner count:

| Trading day | Index rows starting `4` | Distinct accession numbers | Overstatement |
|---|---|---|---|
| 2026-10-14 | 678 | 296 | 2.29x |
| 2026-10-15 | 605 | 292 | 2.07x |
| 2026-10-16 | 912 | 450 | 2.03x |

Dedupe by accession number (the `0001234567-26-123456` token in the file name) and the real counts fall out. The same property is the cheapest joint-filing detector available: because the issuer always contributes exactly one CIK, **a filing with 3+ distinct CIKs in the index is a joint filing**, with no document fetch required.

## Gotcha 2: the joint-filing rate is not a stable number

With that detector, the distribution of CIKs per filing over the same three days:

| CIKs on the filing | 2026-10-14 | 2026-10-15 | 2026-10-16 |
|---|---|---|---|
| 2 (single owner) | 274 | 282 | 444 |
| 3 | 3 | 5 | 2 |
| 4 | 6 | 1 | 3 |
| 5 | 1 | 2 | 0 |
| 6 | 7 | 2 | 1 |
| 8 | 1 | 0 | 0 |
| 9 | 1 | 0 | 0 |
| 11 | 3 | 0 | 0 |
| **Joint (3+ CIKs)** | **22 (7.4%)** | **10 (3.4%)** | **6 (1.3%)** |

Three consecutive trading days, **1,038 Form 4s, 38 joint (3.7% pooled)** — and a per-day rate that moves **5.7x** between the low and the high. 2026-10-14's spike is a handful of large multi-entity control chains landing on the same day: five of that day's joint filings are Blackstone entities reporting on Bumble Inc., including accession `0001193125-26-421982`, which names **ten** reporting owners (`BCP Buzz Holdings L.P.`, `BCP VII Holdings Manager - NQ L.L.C.`, `Blackstone Management Associates VII NQ L.L.C.`, …) on one Form 4. Verified by fetching each joint filing's `ownership.xml` and counting `<reportingOwner>` blocks: the index-derived count and the document agree on all 38.

The practical consequence: **do not quote a joint-filing rate from one day's sample**, yours or ours. We measured 10-16 first, got 1.3%, and would have published a number that the very next sample contradicted by 5.7x.

## Gotcha 3: "the owners' roles differ" is not the bug — the *direction* is

The structural problem with flattening is that a Form 4's role flags (`isDirector`, `isOfficer`, `isTenPercentOwner`, `isOther`, `officerTitle`) live **inside each owner's block**, not on the filing. Read only `reportingOwner[0]` and a role filter — "show me director transactions" — will drop rows whose director is listed second.

But most joint filings cannot trigger that, because most of them give every owner the *same* flags: 32 of the 38 are a control chain in which all owners are 10%-owners (or all directors) and nothing differs at all. Of the **6** whose owners' flag sets do differ, five are an individual listed **first** with their full role set, followed by their holding entities carrying a **subset** (10%-owner only):

```
reportingOwner[0]  Smith Jane     isDirector isOfficer isTenPercentOwner
reportingOwner[1]  Jane Smith LLC            isTenPercentOwner
reportingOwner[2]  Smith Family Trust        isTenPercentOwner
```

A first-owner-only filter reads *more* roles than it should here, not fewer, so nothing is lost. The filings that actually break are the reverse order — first owner missing a role a later owner has. Across all 38 joint filings on these three days, that direction occurred exactly **once**: Apogee Acquisition Corp, accession `0001213900-26-110405`, pulled live while writing this post:

```
reportingOwner[0]  APOGEE ACQUISITION SPONSOR LLC   isTenPercentOwner
reportingOwner[1]  Smith Jeffrey Andrew             isDirector isOfficer isTenPercentOwner
                                                    officerTitle: Chief Executive Officer
```

Ask for `director` transactions on that issuer and a first-owner-only implementation returns **zero rows** — while the filing names a sitting director and CEO who did the trade. The right way to measure this class of bug is to check the *direction* of the difference, not merely that the owners' flag sets differ: a plain "owners differ" test flags 6 of these 38, six times the 1 that can actually lose you a row. Roughly one Form 4 in a few hundred is affected — rare, but it is exactly the filing a role filter is supposed to find.

## What this Actor does with it

- **Role filters match the union of all reporting owners.** `insiderRoles` is tested against the first owner *and* every co-filer, so the Apogee filing above is returned for `insiderRoles: ["director"]` (3 rows) instead of being dropped.
- **Co-filers keep their own flags.** Each row's `coFilers[]` carries that owner's own `isDirector` / `isOfficer` / `isTenPercentOwner` / `isOther` / `officerTitle`, not just a name — so you can tell *which* owner held the role you filtered on, which the filing-level flattening makes impossible.
- **One row per transaction, not per owner.** A joint filing's transactions are reported once, with the owner structure attached, so a joint filing does not inflate your row count (and your bill) by its owner count.

Everything above is reproducible for free without an API key: the daily index is a plain text file, and each filing's `ownership.xml` is a public document. Two requests per joint filing is all the direction check needs, and `https://www.sec.gov` only asks that you send a real `User-Agent`.

## Related guides

- [SEC Form 4 amendments correct real numbers, and no insider-trading Actor's input schema can select them](https://fetchsmith.com/blog/sec-form-4-amendments-are-unselectable)
  — the same filing-shape question one level up: an amended Form 4 is its own form type, not a flag.
- [SEC Form 4's 10b5-1 flag is not spelled "true" — 92% of filings write it as 1 or 0](https://fetchsmith.com/blog/sec-form-4-10b5-1-flag-is-not-a-boolean)
  — the transaction-code and flag-spelling measurement behind this Actor's parser.
- All FetchSmith tools: https://fetchsmith.com/tools

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every number above comes from a live request made while writing this post, not from documentation.*
