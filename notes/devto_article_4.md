# Six ATS job boards publish their jobs as public JSON — and no two agree what a "job" is

Almost every company careers page you've ever seen is a thin wrapper around one of six applicant-tracking systems: Greenhouse, Ashby, Lever, Recruitee, Workable, SmartRecruiters. All six publish the underlying postings as public JSON — no login, no key, no browser. It's the same endpoint the "Apply" button hits.

Finding the endpoints is the easy part. The part that actually costs you a day is that all six disagree about the shape of a job posting — including what the title field is called, whether the response has an envelope at all, and what "remote" is named.

Here's every one of them, with the trap you'll hit. Every field name below came from a live request, not from docs.

## Greenhouse — the description is HTML, but escaped

```
GET https://boards-api.greenhouse.io/v1/boards/airbnb/jobs?content=true
```

Returns `{"jobs": [...]}` — 164 postings for Airbnb when we pulled it.

The trap is `content`. It's real HTML, but **double-encoded**: you get the literal string `&lt;div&gt;…&lt;/div&gt;`, not `<div>…</div>`. Feed that straight into an HTML parser and it sees one flat text node and nothing else. Decode the entities first.

Location is a single free-text `{"name": "..."}` — no city/country split, no remote flag.

## Ashby — the only one with real structured pay

```
GET https://api.ashbyhq.com/posting-api/job-board/ramp?includeCompensation=true
```

Ashby is the richest of the six: `isRemote`, `workplaceType`, and both `descriptionHtml` and `descriptionPlain` pre-split for you. It is also **the only one of the six that reliably publishes numeric salary ranges** — 138 of 145 live postings on Ramp's board carried a real `compensation.summaryComponents[]` entry with `minValue`, `maxValue`, `currencyCode` and `interval`.

The trap: that array also contains non-cash components — `EquityPercentage` and friends — sitting right next to the salary entry, with their numeric fields all null. Take `summaryComponents[0]` blindly and you'll get equity, or nulls. Filter on `compensationType === "Salary"`.

## Lever — no envelope, and the title field isn't `title`

```
GET https://api.lever.co/v0/postings/figma?mode=json
```

Three things at once:

1. The response is a **bare array**. No `{"jobs": …}` wrapper — `[...]` at the top level.
2. The job title lives in a field called **`text`**.
3. Location, team and commitment are folded into a `categories` object rather than top-level fields.

And a lot of company slugs that "should" be on Lever just 404. `plaid`, `brex`, `ramp`, `figma` and `huggingface` all 404 on `api.lever.co` — re-verified live across two separate measurement runs — because they've migrated to another ATS since. A 404 here means *moved*, not *broken*. If you fail the run on it, multi-company jobs will fail more often than they succeed.

## Recruitee — numbers that are strings

```
GET https://<slug>.recruitee.com/api/offers/
```

Recruitee publishes salary, but `salary.min` and `salary.max` come back as **numeric strings**: `"2600"`, not `2600`. Cast them, or every downstream comparison quietly becomes a string comparison — and `"900" > "2600"` is `true`.

## Workable — its own words for two common concepts

```
GET https://apply.workable.com/api/v1/widget/accounts/<slug>?details=true
```

The job identifier is `shortcode`, not `id`. And where the others use some flavor of `isRemote`/`workplaceType`, Workable's remote flag is called **`telecommuting`**. Same concept, different name — trivially dropped if you're mapping fields by convention instead of reading each schema.

## SmartRecruiters — real pagination, but the list has no description

```
GET https://api.smartrecruiters.com/v1/companies/<slug>/postings
```

The only one of the six with proper pagination metadata: `{"offset": 0, "limit": 100, "totalFound": N, "content": [...]}`.

But `content[]` items carry **no job description at all**. Getting the text needs a second call per posting:

```
GET https://api.smartrecruiters.com/v1/companies/<slug>/postings/<id>
```

None of the other five need that. If you're budgeting requests, SmartRecruiters costs you 1 + N instead of 1.

## The three fields that need real normalization

Renaming fields gets you most of the way. Three don't yield to renaming:

**Salary interval.** Greenhouse, Workable and SmartRecruiters don't expose pay at all. Ashby, Lever and Recruitee do — and each spells the period differently. `"1 YEAR"`, `"monthly"`, `"per-year-salary"`, all observed live on the same day. Collapse them to one vocabulary before storing:

```js
const INTERVAL = {
  '1 year': 'year', 'per-year-salary': 'year', 'yearly': 'year', 'annual': 'year',
  '1 month': 'month', 'monthly': 'month', 'per-month-salary': 'month',
  '1 week': 'week', 'weekly': 'week',
  '1 day': 'day', 'daily': 'day',
  '1 hour': 'hour', 'hourly': 'hour', 'per-hour-salary': 'hour',
};
const interval = INTERVAL[String(raw).toLowerCase().trim()] ?? null;
```

This one matters more than it looks. A monthly €2,600 and an annual $211,400 land in the same unlabeled `salaryMin` column looking like the same kind of number. They are not, and nothing downstream will tell you.

**Remote.** `isRemote` (Ashby), `telecommuting` (Workable), and a bare location string with no flag at all (Greenhouse) all mean the same thing to someone filtering for remote work, and no two agree on a name.

**Dead companies.** Covered above — treat a Lever 404 as a skip, not a failure.

## If you'd rather not write the adapter

We maintain [ats-jobs-scraper](https://apify.com/fetchsmith/ats-jobs-scraper), which wraps all six behind one schema — company, ATS source, title, department, team, employment type, workplace type, remote flag, location, normalized salary (min/max/currency/**interval**), timestamps, apply URL and description — and skips companies that have moved ATS instead of failing the run. Pay per posting returned, no start fee, no headless browser for any of the six.

But the endpoints above are public, and there's nothing stopping you building it yourself — that's rather the point of writing them down.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every endpoint and field name above comes from a live request made while writing, not from documentation.*
