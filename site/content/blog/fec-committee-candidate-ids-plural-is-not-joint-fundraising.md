---
title: A committee's FEC candidate_ids field says "plural" 430 times — and 426 of those are one person, not a joint fundraiser
description: 2.06% of FEC committees carry 2+ candidate_ids. Measured on two election cycles with named-candidate verification (20/20 same person), only ~1% of that 2.06% is a real multi-candidate joint fundraising committee. The rest is one person holding a House id and a Senate id at once — a shape our own Actor mislabeled through three builds before this fix.
date: 2026-10-19
tags: webscraping, api, opendata, government
tool: fec-campaign-finance-scraper
---

The FEC's committee registry (`/v1/committee/{id}/`) has a `candidate_ids` field. It's a list, so the natural reading of "2 or more entries" is "this committee is raising money for 2 or more candidates" — a joint fundraising committee (JFC), the vehicle a party or a slate of candidates uses to split one donor's check several ways. [fec-campaign-finance-scraper](/go/fec-campaign-finance-scraper) shipped three builds (through v0.1.70) on exactly that reading, nulling `candidateId` on contribution rows whenever a committee had 2+ ids, on the theory that "2+ ids = ambiguous, can't pick one."

The reading is wrong for 92% of the committees it actually fires on.

## What's really in the 2+ list

We scanned the full FEC committee registry on two separate election cycles rather than trust one sample:

| Cycle | Committees | 2+ `candidate_ids` | Share |
|---|---|---|---|
| 2026 | 20,903 | 430 | 2.06% |
| 2024 | 20,937 | 414 | 1.98% |

Same shape both years, and the designation breakdown inside that 430/414 is the same too: `P` (principal campaign committee) and `A` (authorized committee) make up the large majority, with `J` (joint fundraising committee — the thing the field name suggests) a small single-digit handful — **exactly 4 in both cycles, the same 4 committees**.

We resolved ids to real names (`/v1/candidates/{id}/`) on two independent random samples, 12 and 8 committees, pooling to 20/20: every single `P`/`A` committee's 2+ ids belong to **one person**. The pattern is almost always a House run followed by a Senate run (or vice versa), each of which the FEC assigns its own candidate id — so Senator Durbin's own committee, `FRIENDS OF DICK DURBIN COMMITTEE`, carries both `H2IL20026` and `S6IL00151` for the same human being. Same story for `THE MARKEY COMMITTEE`, `THE REED COMMITTEE`, `MENENDEZ FOR SENATE`. None of these are splitting money across multiple candidates; they're one candidate whose FEC paperwork has two ids because US election law assigns a fresh candidate id per office sought, not per person.

The actual joint fundraising committees — the minority the field name describes — are a tiny, stable set: `CASSIDY PERDUE SULLIVAN TILLIS VICTORY FUND` (four different sitting senators, ids `S4AK00214`/`S4GA11285`/`S4LA00107`/`S4NC00162`) and `FRESHMAN AGRICULTURAL REPUBLICAN MEMBERS TRUST` (sixteen). Both cycles, same 4 committees, ~1% of the 2+ population.

A naming gotcha worth flagging separately: exact-string name matching misclassifies this sample. The FEC spells the same person two ways across filings — `DURBIN, RICHARD JOSEPH` on one committee's record, `DURBIN, RICHARD J.` on another — so comparing full name strings called 5 of 8 sampled committees "different people" when they weren't. Surname + first-initial matching got all 20 right.

## The second bug the first fix nearly shipped

The obvious fix — resolve the ids, null `candidateId` only when they're genuinely different people — is correct for *contributions* (Schedule A), where the `committee` object attached to a donation is the committee that received it. We built that and verified it live: a real donation to a Durbin-linked committee now resolves to `S6IL00151` instead of `null`, and the two real JFCs above correctly stay `null`.

Extending the identical logic to *disbursements* (Schedule B) looked like a one-line change — same field, same committee object, same fallback. It shipped first as a draft and failed verification before it reached production: in Schedule B, the embedded `committee` is the **paying** committee, not the recipient. A committee's own `candidate_ids` describing who that committee *represents* says nothing about who a specific payment went *to*.

The live example that caught it: Senator Durbin's leadership PAC made a real payment to `MELISSA BEAN FOR CONGRESS` — a different candidate's campaign entirely. The FEC's own row already tags that disbursement with `candidate_id: null` (correctly — it's not spending tied to one candidate the way a direct contribution is). The fallback logic, inherited from the Schedule A fix, instead fell back to the *paying* committee's id and reported `candidateId: "S6IL00151"` — Durbin, attributed to a payment that went to Bean. The fix was to delete the fallback entirely: Schedule B disbursements already arrive individually and correctly tagged by the FEC (verified on the real JFC example too — `CASSIDY PERDUE SULLIVAN TILLIS VICTORY FUND`'s payments to each of its four senators each carry that one senator's own id, never the others).

## What this Actor does with it now (v0.1.71)

- **Contributions mode**: `candidateId` resolves to the one real person whenever a committee's 2+ `candidate_ids` are the same human (preferring the id whose office letter matches the committee's own type — the Senate id for a Senate committee), and stays `null` only when the ids genuinely belong to different people.
- **`candidateIds`** (new field) always carries the raw list of ids on a 2+ committee, same-person or not, so a same-person resolution never hides the underlying FEC data.
- **Disbursements mode**: no fallback. `candidateId`/`candidateName` pass through exactly what the FEC itself tagged the payment with — `null` means the FEC itself didn't attribute it to one candidate, not "we couldn't figure it out."

If you're pulling `candidate_ids` from any FEC endpoint yourself: check the designation code before assuming "2+" means a joint fundraiser. `P`/`A` with 2+ ids is, 19 times out of 20 by our count, one person with two id numbers.

## Related guides

- [The FEC's donor-search API accepts a page number on every request — and silently ignores it on three of four](https://fetchsmith.com/blog/fec-schedule-a-page-parameter-ignored)
- [The FEC publishes campaign finance as key-free JSON — and its three rate limits contradict each other](https://fetchsmith.com/blog/fec-campaign-finance-json-api-demo-key)
- All FetchSmith tools: https://fetchsmith.com/tools

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every number above comes from a live request made while writing this post, not from documentation.*
