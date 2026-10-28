import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
// Soft-deadline guard (cycle 1736, 4th Actor on the rollout; same pattern as fda-recall-scraper /
// nih-reporter-scraper / court-records-scraper): a hard platform kill mid-walk skips the
// RUN_SUMMARY write and, in watch mode, the baseline save -- the buyer loses their seed and gets
// re-billed for everything past the cutoff on the next run. Stop proactively with a safety margin
// instead, and report it as 'time-budget', not as a ClinicalTrials.gov failure. `apiGet`'s
// retry/Retry-After sleeps are the thing most likely to overrun the run's own timeout.
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
function timeBudgetOk() { return remainingMs() > 0; }
let timeBudgetExceeded = false;
function failureReason(fallback) { return timeBudgetExceeded ? 'time-budget' : fallback; }

const input = (await Actor.getInput()) ?? {};

// ---------------------------------------------------------------------------
// `startUrl` -- paste a ClinicalTrials.gov search URL instead of re-typing its filters by hand.
// Two shapes are accepted (both verified live, cycle 376):
//   * the search page -- https://clinicaltrials.gov/search?cond=asthma&aggFilters=status:rec,phase:3
//   * the public API  -- https://clinicaltrials.gov/api/v2/studies?query.cond=asthma&aggFilters=...
// The search page's parameter names are taken from the site's own search app (its analytics map
// labels every one: cond/term/locn/intr/outc/lead/titles/spons/id, and the date windows
// start/firstPost/lastUpdPost/studyComp/primComp/resFirstPost, each `from_to` with an underscore
// and either side optional).
//
// `aggFilters` is forwarded VERBATIM rather than decoded into our typed inputs and re-encoded:
// all ten codes the UI can emit (status, phase, studyType, funderType, sex, healthy, ages,
// results, docs, violation) were checked live against the API this cycle and every one is accepted
// and narrows the result count, so a pass-through cannot lose a filter the way a partial decoder
// would silently drop an unknown one.
//
// Enum audit (cycle 816, live against the v2 API, no filter but the one under test): every value
// in every enum we expose is real and non-empty registry-wide -- all 14 `overallStatus`
// (TEMPORARILY_NOT_AVAILABLE is the rarest at 36 studies, WITHHELD 983, APPROVED_FOR_MARKETING
// 241, AVAILABLE 255, NO_LONGER_AVAILABLE 536), all 3 `studyTypes` (EXPANDED_ACCESS 1,068), all 6
// `phases`, all 3 `ageGroups`, all 3 `documentTypes` (union 56,182 = 9.3% of 604,566 studies, so
// the README's "about 9%" still holds), both `resultsAvailability` values and both `sex` values.
// No structurally-dead value to remove. Two schema descriptions WERE stale and were corrected:
// `fdaRegulationViolation` said "a few dozen" (really 8 -- the README already had this right), and
// `phases` said "~19% of all studies have no phase at all (observational studies, device trials)"
// -- really 23.7% (143,294), and the breakdown is 141,118 observational + 1,068 expanded-access
// + 983 withheld + only 125 interventional, i.e. interventional device/behavioral trials are NOT
// phase-less, they are phase NA (237,522 of them). The old wording sent those users to the wrong
// control.
//
// Precedence: a `startUrl` is the source of truth for the filters it carries. The search-term
// family (cond/term/intr/spons/locn/titles/outc/lead/id) is REPLACED wholesale -- set to the URL's
// values, cleared where the URL has none -- because `conditions` has a schema default ("cancer")
// that the platform fills in for any run that omits it, and silently AND-ing that default into a
// pasted URL's search would quietly return the wrong studies. Every other input the URL does not
// mention (maxResults, rowsPerStudy, watchLabel, hand-set dates/ages/status/sort) still applies.
// If the URL's aggFilters DOES carry a status/phase/studyType/sex/healthy/ages/funderType code
// AND the matching typed input is also set, the typed input wins outright (its own code is
// dropped from the URL's aggFilters below) rather than ANDing the two into a silent contradiction
// -- fixed cycle 1325 after a startUrl's `aggFilters=status:rec` plus a typed
// `overallStatus:["COMPLETED"]` verified live to return 0 rows with no warning explaining why.
const urlAggFilters = new Map();
applyStartUrl(input.startUrl);

function applyStartUrl(raw) {
    const s = String(raw ?? '').trim();
    if (!s) return;
    let u;
    try { u = new URL(s); } catch { throw new Error(`"startUrl" is not a valid URL: ${s}`); }
    if (!/(^|\.)clinicaltrials\.gov$/i.test(u.hostname)) {
        throw new Error(`"startUrl" must be a clinicaltrials.gov search or API URL (got "${u.hostname}").`);
    }
    const q = u.searchParams;
    const filled = [];
    // Set a field from the URL. An empty URL value leaves the caller's own value alone.
    const fill = (field, value) => {
        if (value === undefined || value === null || value === '') return;
        input[field] = value;
        filled.push(field);
    };

    const UI_TEXT = {
        cond: 'conditions',
        term: 'searchQuery',
        intr: 'interventions',
        spons: 'sponsors',
        locn: 'locations',
        titles: 'titleOrAcronym',
        outc: 'outcomeMeasure',
        lead: 'leadSponsorName',
        id: 'nctIds',
    };
    const API_TEXT = {
        'query.cond': 'conditions',
        'query.term': 'searchQuery',
        'query.intr': 'interventions',
        'query.spons': 'sponsors',
        'query.locn': 'locations',
        'query.titles': 'titleOrAcronym',
        'query.outc': 'outcomeMeasure',
        'filter.ids': 'nctIds',
    };
    // UI date-window param -> our [from, to] input pair.
    const UI_DATES = {
        start: ['studyStartDateFrom', 'studyStartDateTo'],
        primComp: ['primaryCompletionDateFrom', 'primaryCompletionDateTo'],
        studyComp: ['studyCompletionDateFrom', 'studyCompletionDateTo'],
        firstPost: ['firstPostedDateFrom', 'firstPostedDateTo'],
        resFirstPost: ['resultsFirstPostedDateFrom', 'resultsFirstPostedDateTo'],
        lastUpdPost: ['lastUpdatePostedDateFrom', 'lastUpdatePostedDateTo'],
    };

    // Search-term family: replaced wholesale (see the precedence note above), so clear first.
    for (const field of new Set([...Object.values(UI_TEXT), ...Object.values(API_TEXT)])) {
        input[field] = '';
    }
    for (const [param, field] of Object.entries({ ...UI_TEXT, ...API_TEXT })) {
        fill(field, (q.get(param) ?? '').trim());
    }
    for (const [param, [from, to]] of Object.entries(UI_DATES)) {
        const [f = '', t = ''] = (q.get(param) ?? '').split('_');
        fill(from, f.trim());
        fill(to, t.trim());
    }
    // API-shaped URLs carry status as a comma list and sort as one string; both reuse the same
    // whitelists the hand-typed inputs go through below, so a junk value can't reach the API.
    const statusParam = (q.get('filter.overallStatus') ?? '').trim();
    if (statusParam) fill('overallStatus', statusParam.split(/[\s,]+/).filter(Boolean));
    fill('sortBy', (q.get('sort') ?? '').trim());

    // UI age range: "18y_65y" (unit letter optional — y/m/w/d, defaulting to years — either side
    // optional). The letter maps onto the same unit the API takes, so "6m_" is carried through as
    // 6 Months rather than being dropped; an unrecognised letter is reported and skipped.
    const UI_AGE_UNITS = { y: 'Years', m: 'Months', w: 'Weeks', d: 'Days' };
    const [ageFrom = '', ageTo = ''] = (q.get('ageRange') ?? '').split('_');
    for (const [rawAge, field, unitField] of [
        [ageFrom, 'ageRangeFromYears', 'ageRangeFromUnit'],
        [ageTo, 'ageRangeToYears', 'ageRangeToUnit'],
    ]) {
        const a = rawAge.trim();
        if (!a) continue;
        const m = /^(\d+)\s*([a-zA-Z]*)$/.exec(a);
        const unit = m && (m[2] ? UI_AGE_UNITS[m[2].toLowerCase()] : 'Years');
        if (!unit) {
            log.warning(`startUrl ageRange bound "${a}" has no recognised unit (y/m/w/d); ignoring that bound.`);
            continue;
        }
        fill(field, Number(m[1]));
        fill(unitField, unit);
    }

    for (const pair of (q.get('aggFilters') ?? '').split(',')) {
        const idx = pair.indexOf(':');
        if (idx <= 0) continue;
        const key = pair.slice(0, idx).trim();
        const value = pair.slice(idx + 1).trim();
        if (key && value) urlAggFilters.set(key, value);
    }

    const aggDesc = urlAggFilters.size ? ` + aggFilters ${[...urlAggFilters.keys()].join('/')}` : '';
    log.info(`startUrl parsed: filled ${filled.length ? filled.join(', ') : 'nothing'}${aggDesc}.`);
    if (!filled.length && !urlAggFilters.size) {
        log.warning('startUrl carried no filters this Actor understands -- the run will use the other inputs only.');
    }
}

// ClinicalTrials.gov's own official API v2 (NIH/NLM). No API key, no auth, no proxy.
const API = 'https://clinicaltrials.gov/api/v2/studies';

// Verified live (cycle 120): pageSize=1000 works, pageSize=1001 returns HTTP 200 with only
// 1000 rows — a SILENT cap, not a 400 like the Federal Register / openFDA APIs. Never pass a
// caller-supplied pageSize straight through; always clamp to this.
const MAX_PAGE_SIZE = 1000;

const STATUSES = new Set([
    'RECRUITING', 'NOT_YET_RECRUITING', 'ENROLLING_BY_INVITATION', 'ACTIVE_NOT_RECRUITING',
    'COMPLETED', 'TERMINATED', 'WITHDRAWN', 'SUSPENDED', 'UNKNOWN', 'WITHHELD', 'AVAILABLE',
    'NO_LONGER_AVAILABLE', 'APPROVED_FOR_MARKETING', 'TEMPORARILY_NOT_AVAILABLE',
]);
const STUDY_TYPES = new Set(['INTERVENTIONAL', 'OBSERVATIONAL', 'EXPANDED_ACCESS']);
const PHASES = new Set(['EARLY_PHASE1', 'PHASE1', 'PHASE2', 'PHASE3', 'PHASE4', 'NA']);

const cleanList = (v, allowed) => (Array.isArray(v) ? v : [])
    .map((x) => String(x).toUpperCase().trim())
    .filter((x) => !allowed || allowed.has(x));

const NCT_RE = /^NCT\d{8}$/;
const nctIdsRaw = String(input.nctIds ?? '').split(/[\s,]+/).map((s) => s.trim().toUpperCase()).filter(Boolean);
const nctIds = [...new Set(nctIdsRaw.filter((id) => NCT_RE.test(id)))];
const nctIdsBadFormat = nctIdsRaw.filter((id) => !NCT_RE.test(id));
if (nctIdsBadFormat.length) {
    log.warning(`Dropped ${nctIdsBadFormat.length} nctIds with bad format (expected NCT + 8 digits): ${nctIdsBadFormat.join(', ')}`);
}
// If EVERY supplied id was dropped, `nctIds` is empty and the dispatch below silently falls out of
// direct-lookup into SEARCH mode -- and `conditions` carries a schema default of "cancer" that
// Apify applies server-side to any input missing the field (see the resolveIdsChunk note), so
// someone who asked for two specific trials would instead be delivered, and charged for, up to
// `maxResults` arbitrary cancer studies. Nothing is charged yet at this point, so fail on the
// input error exactly like the other input-validation throws above/below rather than running a
// query the buyer never asked for. (cycle 2352)
if (nctIdsRaw.length && !nctIds.length) {
    throw new Error(
        `Every value in "nctIds" was rejected as malformed (expected NCT followed by 8 digits, e.g. NCT04280705): `
        + `${nctIdsBadFormat.join(', ')}. Fix the ids and re-run -- the run was stopped instead of falling back to a `
        + 'filter search, which would have returned studies you did not ask for and charged you for them.',
    );
}

let conditions = String(input.conditions ?? '').trim();
const interventions = String(input.interventions ?? '').trim();
const sponsors = String(input.sponsors ?? '').trim();
const locations = String(input.locations ?? '').trim();
const searchQuery = String(input.searchQuery ?? '').trim();
const overallStatus = cleanList(input.overallStatus, STATUSES);
const studyTypes = cleanList(input.studyTypes, STUDY_TYPES);
const phases = cleanList(input.phases, PHASES);
const hasResultsOnly = input.hasResultsOnly === true;
// `resultsAvailability` supersedes the older boolean `hasResultsOnly`; the boolean is kept as a
// legacy fallback so saved inputs / scheduled runs from before this field existed keep working.
const RESULTS_AVAILABILITY = new Set(['with', 'without']);
const resultsAvailability = RESULTS_AVAILABILITY.has(String(input.resultsAvailability ?? '').trim())
    ? String(input.resultsAvailability).trim()
    : (hasResultsOnly ? 'with' : '');
const sex = ['FEMALE', 'MALE'].includes(String(input.sex ?? '').toUpperCase()) ? String(input.sex).toUpperCase() : '';
const acceptsHealthyVolunteers = input.acceptsHealthyVolunteers === true;
const includeStopReason = input.includeStopReason !== false;
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
// A non-empty value that fails DATE_RE must never be silently dropped: `DATE_RE.test(x) ? x : ''`
// (the shape this replaced) looks identical to "field left empty" for a WIDENED window, not a
// narrowed one, so a typo'd date silently loses its bound, returns MORE studies than asked for,
// and bills for them -- the same defect class `sec-insider-trades-scraper` had in `sinceDate`
// (cycle 2016), except this file has 6 date-pair fields sharing the bug, not 1. Throwing here
// matches this fleet's dominant convention for a malformed date bound (ats-jobs-scraper,
// remote-jobs-scraper, nih-reporter-scraper, apple-podcasts-scraper, uk-find-a-tender-scraper,
// court-records-scraper, app-store-reviews-scraper, grants-gov-scraper, fec-campaign-finance-
// scraper all fail loudly rather than guess) over sec-insider-trades-scraper's warn-and-ignore,
// which that Actor's README explicitly documents as "leave empty for no lower bound" semantics
// this file's README does not promise.
const parseDateBound = (raw, field) => {
    const s = String(raw ?? '').trim();
    if (!s) return '';
    if (!DATE_RE.test(s)) {
        throw new Error(`"${field}" is not a real calendar date: ${JSON.stringify(raw)}. Use YYYY-MM-DD, e.g. 2026-08-01.`);
    }
    return s;
};
// Every date filter is the same shape: two ISO dates that become one AREA[<field>]RANGE[from,to]
// clause (MIN/MAX for an open bound). `area` is the ClinicalTrials.gov advanced-filter area name;
// all six were verified live against the real API before being wired up — a wrong area name is a
// hard 400 ("Unknown area name"), never a silently-ignored filter, so a typo here cannot ship as
// "filter had no effect".
const DATE_FILTERS = [
    { from: 'lastUpdatePostedDateFrom', to: 'lastUpdatePostedDateTo', area: 'LastUpdatePostDate' },
    { from: 'studyStartDateFrom', to: 'studyStartDateTo', area: 'StartDate' },
    { from: 'primaryCompletionDateFrom', to: 'primaryCompletionDateTo', area: 'PrimaryCompletionDate' },
    { from: 'studyCompletionDateFrom', to: 'studyCompletionDateTo', area: 'CompletionDate' },
    { from: 'firstPostedDateFrom', to: 'firstPostedDateTo', area: 'StudyFirstPostDate' },
    { from: 'resultsFirstPostedDateFrom', to: 'resultsFirstPostedDateTo', area: 'ResultsFirstPostDate' },
];
const dateRanges = [];
const dateCriteria = {};
for (const { from, to, area } of DATE_FILTERS) {
    const f = parseDateBound(input[from], from);
    const t = parseDateBound(input[to], to);
    if (f && t && f > t) {
        throw new Error(`"${from}" (${f}) is after "${to}" (${t}) — the window is empty. Swap them.`);
    }
    if (f || t) dateRanges.push(`AREA[${area}]RANGE[${f || 'MIN'},${t || 'MAX'}]`);
    dateCriteria[from] = f || null;
    dateCriteria[to] = t || null;
}
// `resultsAvailability="without"` asks for studies that have posted NO results section; every
// `resultsFirstPostedDate*` bound asks for a study whose results were first posted inside a window.
// A study with no results section has no ResultsFirstPostDate at all, so the two can never both
// hold — same shape as the ageRange from>to contradiction below, and verified live registry-wide
// (not just reasoned): `aggFilters=results:without` alone = 524,648 studies, the widest possible
// `AREA[ResultsFirstPostDate]RANGE[1900-01-01,2100-01-01]` alone = 80,302, the two together = 0,
// as is an open-ended `RANGE[1900-01-01,MAX]` and a `RANGE[MIN,<to>]`. Before this check the run
// just returned 0 rows and fell through to the generic "no studies matched" advice, which names
// three other causes but not this one — so the buyer was told to widen a condition that was never
// the problem. `resultsAvailability="with"` + the same window is NOT a contradiction (it is merely
// redundant: 266 = 266 on query.cond=asthma), so only "without" is rejected.
if (resultsAvailability === 'without' && (dateCriteria.resultsFirstPostedDateFrom || dateCriteria.resultsFirstPostedDateTo)) {
    const bound = dateCriteria.resultsFirstPostedDateFrom
        ? `resultsFirstPostedDateFrom (${dateCriteria.resultsFirstPostedDateFrom})`
        : `resultsFirstPostedDateTo (${dateCriteria.resultsFirstPostedDateTo})`;
    throw new Error(
        `"resultsAvailability" is "without" (studies that have posted NO results) but "${bound}" filters on the date `
        + 'those results were first posted — a study with no results has no results-posted date, so no study can ever '
        + 'satisfy both and the run would return 0 rows. Either set resultsAvailability to "with" (or leave it blank) '
        + 'to use the date window, or clear the resultsFirstPostedDate filters to list studies without results.',
    );
}
// Kept as named bindings because the run-summary log line below reports them explicitly.
const lastUpdatePostedDateFrom = parseDateBound(input.lastUpdatePostedDateFrom, 'lastUpdatePostedDateFrom');
const lastUpdatePostedDateTo = parseDateBound(input.lastUpdatePostedDateTo, 'lastUpdatePostedDateTo');
const FUNDER_TYPES = new Set(['NIH', 'FED', 'OTHER_GOV', 'INDUSTRY', 'NETWORK', 'INDIV', 'OTHER', 'UNKNOWN', 'AMBIG']);
const funderTypes = cleanList(input.funderTypes, FUNDER_TYPES);
// Verified live: AREA[MinimumAge]/AREA[MaximumAge] RANGE take "<n> <Unit>" (or MIN/MAX for an
// open bound) — same RANGE syntax as the date fields above, just a different unit string.
// Verified live on query.cond=cancer: "0 Years" -> 115629, "6 Months" -> 114908, "3 Weeks" ->
// 115213, "10 Days" -> 115227 — four different counts, so sub-year units really are honoured.
// An unknown unit is a hard 400 ("No enum constant ...TimeParts.Unit"), so this must stay a
// strict whitelist; anything else falls back to the historical Years behaviour.
const AGE_UNITS = new Set(['Years', 'Months', 'Weeks', 'Days']);
const ageUnit = (raw) => {
    const u = String(raw ?? '').trim().toLowerCase();
    for (const known of AGE_UNITS) if (known.toLowerCase() === u) return known;
    return 'Years';
};
const ageRangeFromUnit = ageUnit(input.ageRangeFromUnit);
const ageRangeToUnit = ageUnit(input.ageRangeToUnit);
const ageRangeFromYears = Number.isInteger(input.ageRangeFromYears) && input.ageRangeFromYears >= 0 ? input.ageRangeFromYears : null;
const ageRangeToYears = Number.isInteger(input.ageRangeToYears) && input.ageRangeToYears >= 0 ? input.ageRangeToYears : null;
if (ageRangeFromYears !== null && ageRangeToYears !== null && ageRangeFromYears > ageRangeToYears
    && ageRangeFromUnit === ageRangeToUnit) {
    // Verified live: a study's own MaximumAge must be >= its own MinimumAge, so requiring
    // MinimumAge >= ageRangeFrom AND MaximumAge <= ageRangeTo with from > to in the SAME unit is a
    // contradiction no study can ever satisfy — confirmed empty on a real API call, not just reasoned.
    // Across different units it is NOT a contradiction, verified live: "from 1 Years, to 12 Months"
    // returns 13 real studies registry-wide (studies enrolling exactly one-year-olds, where the two
    // bounds meet), so mixed units only warn rather than fail the run — throwing would have blocked
    // a legitimate query.
    throw new Error(
        `"ageRangeFromYears" (${ageRangeFromYears} ${ageRangeFromUnit}) is greater than "ageRangeToYears" (${ageRangeToYears} ${ageRangeToUnit}) — no study's eligibility range can ever satisfy both. Swap them.`,
    );
}
if (ageRangeFromYears !== null && ageRangeToYears !== null && ageRangeFromUnit !== ageRangeToUnit) {
    log.warning(
        `Age bounds use different units (from ${ageRangeFromYears} ${ageRangeFromUnit}, to ${ageRangeToYears} ${ageRangeToUnit}) — `
        + 'both are sent as-is, but check the order is what you meant if the run returns 0 rows.',
    );
}
// Verified live: AREA[StdAge](CHILD OR OLDER_ADULT) returns exactly the same totalCount as the
// UI's `aggFilters=ages:child older` (119,295 on query.cond=cancer) — same filter, and the AREA
// form composes with AND inside the existing filter.advanced string, so no extra param needed.
const AGE_GROUPS = new Set(['CHILD', 'ADULT', 'OLDER_ADULT']);
const ageGroups = cleanList(input.ageGroups, AGE_GROUPS);
// A startUrl's aggFilters can carry status/phase/studyType/sex/healthy/ages/funderType codes
// (see the precedence note above), but those 7 typed inputs are sent via filter.overallStatus /
// AREA[...] (baseParams below), NOT via the aggFilters Map -- unlike docs/results/violation,
// which share that Map and so already get overwritten there by key. Without this, a startUrl
// carrying aggFilters=status:rec plus a typed overallStatus=[COMPLETED] AND together into a
// silent 0-row contradiction instead of the typed value winning as the precedence note promises
// (verified live, cycle 1325: declaredMatches=0, the generic "No studies matched" advice never
// mentions this cause). Clearing the URL's code here makes the typed input win outright, same as
// docs/results/violation already do.
if (overallStatus.length) urlAggFilters.delete('status');
if (phases.length) urlAggFilters.delete('phase');
if (studyTypes.length) urlAggFilters.delete('studyType');
if (sex) urlAggFilters.delete('sex');
if (acceptsHealthyVolunteers) urlAggFilters.delete('healthy');
if (ageGroups.length) urlAggFilters.delete('ages');
if (funderTypes.length) urlAggFilters.delete('funderType');
// Study-document filter. Values are the UI's lowercase codes, OR-ed by SPACE inside one
// aggFilters pair (`docs:sap prot`); a comma there is a 400, and an unknown code is NOT an
// error — it silently returns 0 rows — so this list must stay a strict whitelist.
const DOCUMENT_TYPES = new Set(['prot', 'sap', 'icf']);
const documentTypes = (Array.isArray(input.documentTypes) ? input.documentTypes : [])
    .map((x) => String(x).toLowerCase().trim())
    .filter((x) => DOCUMENT_TYPES.has(x));
// Only `violation:y` is a real value (`violation:n` silently returns 0), so this is a boolean.
const fdaRegulationViolation = input.fdaRegulationViolation === true;
// The final set of aggFilters codes this run actually sends (startUrl-sourced codes not already
// overridden by a typed input above, plus the three typed inputs that share the same Map). Built
// ONCE here, rather than inline inside baseParams() below, so watchCriteria (next block) can
// fingerprint exactly what the live query sends -- see the comment there for why that matters.
const effectiveAggFilters = new Map(urlAggFilters);
if (resultsAvailability) effectiveAggFilters.set('results', resultsAvailability);
if (documentTypes.length) effectiveAggFilters.set('docs', documentTypes.join(' '));
if (fdaRegulationViolation) effectiveAggFilters.set('violation', 'y');
const titleOrAcronym = String(input.titleOrAcronym ?? '').trim();
const outcomeMeasure = String(input.outcomeMeasure ?? '').trim();
// An AREA(...) term is parsed as a query expression, so a multi-word value has to be quoted to
// stay one phrase (verified live: AREA[LocationFacility](Mayo Clinic) = 3,717 hits on cond=cancer
// vs AREA[LocationFacility]("Mayo Clinic") = 3,708 — the unquoted form is two loose terms, not the
// facility name). Double quotes and backslashes inside the value are dropped rather than escaped:
// neither is ever part of a real facility or sponsor name, and leaving them in can unbalance the
// quoting and turn a narrow search into a 400 or a wrong-filter result.
const areaPhrase = (s) => `"${s.replace(/["\\]/g, ' ').replace(/\s+/g, ' ').trim()}"`;
const facilityName = String(input.facilityName ?? '').trim();
const leadSponsorName = String(input.leadSponsorName ?? '').trim();
const SORT_VALUES = new Set(['LastUpdatePostDate:desc', 'StudyFirstPostDate:desc', 'EnrollmentCount:desc']);
const sortBy = SORT_VALUES.has(input.sortBy) ? input.sortBy : '';
const rowsPerStudy = input.rowsPerStudy === 'site' ? 'site' : 'study';
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 50000);
const watchLabel = String(input.watchLabel ?? '').trim();
const watchMode = watchLabel.length > 0 && nctIds.length === 0;
const watchChanges = Boolean(input.watchChanges);

// Convenience completion ping (same shape as grants-gov-scraper, cycle 421). A bad value is
// warned and ignored rather than thrown -- this is a notification nicety, not core function.
const webhookUrlRaw = String(input.webhookUrl ?? '').trim();
let webhookUrl = null;
if (webhookUrlRaw) {
    try {
        const parsed = new URL(webhookUrlRaw);
        if (parsed.protocol === 'http:' || parsed.protocol === 'https:') webhookUrl = parsed.toString();
        else log.warning(`webhookUrl "${webhookUrlRaw}" is not http(s); ignoring.`);
    } catch {
        log.warning(`webhookUrl "${webhookUrlRaw}" is not a valid URL; ignoring.`);
    }
}
if (input.watchLabel && nctIds.length) {
    log.warning(
        'watchLabel is ignored when nctIds is set -- direct-lookup mode always returns exactly the ids you '
        + 'asked for, so there is no "new since last run" concept to track for it.',
    );
}

// SITE-MODE SCOPE DISCLOSURE (added cycle 2260). `facilityName` (AREA[LocationFacility]) and
// `locations` (query.locn) are STUDY-level filters: they select studies that have at least one
// matching site, and ClinicalTrials.gov exposes no site-level filter at all (same root cause as
// the site.status FAQ). emitStudy() then explodes EVERY site of each matching study into its own
// charged row, so in site mode the great majority of delivered rows can be facilities that do not
// match what the buyer typed. Measured live 2026-10-26 on `conditions:"cancer"` +
// `facilityName:"Mayo Clinic"`: the first 10 matched studies hold 1,105 sites of which 18 (1.6%)
// are actually Mayo Clinic, and a default `maxResults:100` run never gets past the first study or
// two. The README steers site-selection buyers at exactly this combination, so saying nothing
// here bills them ~98% rows they did not ask for and looks like a broken filter. Not a filter
// change: dropping the non-matching sites would silently remove data existing buyers may rely on
// (the co-site list is the point for some), so disclose and let them filter `site.facility`.
const siteScopeIgnored = [];
if (rowsPerStudy === 'site') {
    if (facilityName) siteScopeIgnored.push(`facilityName="${facilityName}"`);
    if (locations) siteScopeIgnored.push(`locations="${locations}"`);
}
if (siteScopeIgnored.length) {
    log.warning(
        `${siteScopeIgnored.join(' and ')} ${siteScopeIgnored.length > 1 ? 'select' : 'selects'} STUDIES, `
        + 'not sites -- ClinicalTrials.gov has no site-level '
        + 'filter. rowsPerStudy="site" then returns (and CHARGES for) every site of each matching study, '
        + 'including facilities that do not match what you typed: on a live cancer + "Mayo Clinic" check, '
        + 'only 1.6% of the site rows were Mayo Clinic facilities. Filter `site.facility` on the returned '
        + 'rows yourself, and note maxResults counts SITE rows here, so a large multi-site trial can use up '
        + 'your whole cap on its own.',
    );
}

// THE DEFAULT-NARROWING TRAP (same class as nih-reporter-scraper's `keyword`, cycle 1904/1906;
// same shape as the cycle-893/894/895 default-injection bug but in its narrowing form).
// `conditions` used to carry a schema `default` of "cancer", which Apify merges into ANY run that
// omits the field (API/CLI/scheduler/webhook, not just a Console click), and `baseParams()` ANDs
// `conditions` into `query.cond` on every call that isn't a direct nctIds lookup. So
// `{"sponsors":"Pfizer"}` -- the natural way to ask "all Pfizer-sponsored trials" -- silently
// returned only Pfizer's CANCER trials. Measured live against ClinicalTrials.gov's own API before
// shipping this fix: `query.spons=Pfizer` alone declares 6,095 studies; the same call with
// `query.cond=cancer` added declares only 1,459 -- and `query.spons` on its own filters correctly
// (no court-records-style masked interaction where dropping one field breaks another), so this is
// a plain narrowing bug, safe to fix the established way.
// FIX, same shape as nih-reporter's: the default lives in CODE, not the schema (schema keeps its
// own `prefill` so the Console form still shows "breast cancer" and submits it explicitly), and is
// applied ONLY when the field is truly absent AND the run has no other scope at all -- i.e. the
// bare `{}` run Apify's automated Store default-input gate makes (PLAYBOOK, cycle 96) still
// returns real cancer rows, while any caller who names a scope of their own gets exactly that
// scope. `input.conditions === undefined` is the discriminator: an explicit "" is a deliberate
// "no condition filter" and must stay empty.
const CONDITIONS_DEFAULT = 'cancer';
const otherScope = nctIds.length > 0 || Boolean(interventions) || Boolean(sponsors) || Boolean(locations)
    || Boolean(searchQuery) || Boolean(titleOrAcronym) || Boolean(outcomeMeasure) || overallStatus.length > 0
    || studyTypes.length > 0 || phases.length > 0 || Boolean(resultsAvailability) || Boolean(sex)
    || acceptsHealthyVolunteers || dateRanges.length > 0 || funderTypes.length > 0 || ageGroups.length > 0
    || documentTypes.length > 0 || fdaRegulationViolation || Boolean(facilityName) || Boolean(leadSponsorName)
    || ageRangeFromYears !== null || ageRangeToYears !== null;
if (input.conditions === undefined && !otherScope) {
    conditions = CONDITIONS_DEFAULT;
    log.info(
        `No conditions and no other filter was given, so this run uses the example condition "${CONDITIONS_DEFAULT}". `
        + 'Set "conditions" to search for something else, or add any other filter (interventions, sponsors, '
        + 'locations, overallStatus, phases, a date window, etc.) to search without a condition.',
    );
}

// ---------------------------------------------------------------------------
// Watch mode: "only what is new since my last run", per saved query. Same shape as
// fda-recall-scraper (cycle 299) / grants-gov-scraper (cycle 298) / federal-register-scraper
// (cycle 297) / nih-reporter-scraper (cycle 296) -- copy that design, don't reinvent it.
//
// The baseline is the buyer's own -- the nctIds this label has already delivered -- kept in a
// NAMED key-value store on the buyer's own account (the default KV store is per-run and would
// reset the baseline every run, i.e. re-charge the whole result set on every scheduled run).
const WATCH_STORE = 'fetchsmith-clinicaltrials-watch';
const SEED_CAP = 20000; // our own bound on a seed walk's runtime, not a server limit
const WATCH_KEEP = 60000; // bound the record size; oldest ids fall off first
let baselineTruncated = 0; // ids dropped by WATCH_KEEP this run -- they come back as "new" and get charged
let baselineTruncatedTotal = 0; // same, cumulative over the life of this label

// None of the six date-range pairs above resolve a rolling/relative default (verified against
// `.actor/input_schema.json`: no `default` on any of them, unlike federal-register-scraper's
// last-90-days or fda-recall-scraper's last-365-days) -- `dateCriteria` already holds the buyer's
// own explicit input (or null), never a computed value, so fingerprinting it directly is safe.
//
// BUG FOUND AND FIXED (cycle 2205, `varied_test`): a `startUrl`'s `aggFilters` codes that have no
// typed-input override (e.g. `aggFilters=status:rec` with `overallStatus` left unset) used to be
// completely invisible to this fingerprint -- `resultsAvailability`/`documentTypes`/
// `fdaRegulationViolation` were already fingerprinted via their OWN typed fields above, but the
// other 7 codes (status/phase/studyType/sex/healthy/ages/funderType) only existed in
// `urlAggFilters`, which this object never read. Proven live: two runs sharing one `watchLabel`,
// identical `conditions:"melanoma"` and no typed `overallStatus`, differing ONLY in
// `startUrl`'s `aggFilters` (`status:rec` vs `status:com` -- 483 vs 1,751 real, disjoint
// studies) hashed to the SAME watchKey. Run 2 came back `mode:"watch-incremental"` instead of
// the free `"watch-seed"` a genuinely new saved search should get, delivered+CHARGED 3 rows, and
// merged two disjoint study populations into one baseline (`baselineSize` 483 -> 486). Fixed by
// fingerprinting `effectiveAggFilters` (computed once, above, and now shared with `baseParams()`
// so the two can never drift apart again) -- empty for every run that doesn't hit this path, so
// no existing baseline's fingerprint changes (same `ageRangeFromUnit` precedent as cycle 400:
// only spread in a value that can shift the hash when it is genuinely non-default).
const watchCriteria = {
    conditions, interventions, sponsors, locations, searchQuery, titleOrAcronym, outcomeMeasure,
    overallStatus: [...overallStatus].sort(),
    studyTypes: [...studyTypes].sort(),
    phases: [...phases].sort(),
    resultsAvailability,
    documentTypes: [...documentTypes].sort(),
    fdaRegulationViolation,
    ...(effectiveAggFilters.size ? { aggFilters: [...effectiveAggFilters].map(([k, v]) => `${k}:${v}`).sort() } : {}),
    sex,
    acceptsHealthyVolunteers,
    funderTypes: [...funderTypes].sort(),
    ageGroups: [...ageGroups].sort(),
    ageRangeFromYears,
    ageRangeToYears,
    // Spread in only when non-default: writing "Years" on the default path would change the
    // fingerprint of every existing watch baseline and silently reset them all once (cycle 400).
    ...(ageRangeFromUnit !== 'Years' ? { ageRangeFromUnit } : {}),
    ...(ageRangeToUnit !== 'Years' ? { ageRangeToUnit } : {}),
    facilityName,
    leadSponsorName,
    ...dateCriteria,
};

function watchKeyFor(label, criteria) {
    const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
    const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
    return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let changedCount = 0;
// nctId -> last-seen snapshot of thin fields (already fetched, no extra API calls) that can
// change on an otherwise-already-delivered study: lastUpdatePostDate (ClinicalTrials.gov's own
// "this record changed" signal), overallStatus (e.g. Recruiting -> Completed/Terminated),
// enrollmentCount (revised target) and primaryCompletionDate/completionDate (readout date
// slips). `watchChanges` decides whether a change re-delivers the row; the snapshot itself is
// always kept current so turning the flag on later detects only future drift, not a backlog
// since the baseline. Same shape as us-federal-awards-scraper's `watchChanges` (cycle 349) --
// copy, don't reinvent.
const watchSeen = new Map();

function snapshotOf(row) {
    return {
        lastUpdatePostDate: row.lastUpdatePostDate ?? null,
        overallStatus: row.overallStatus ?? null,
        enrollmentCount: row.enrollmentCount ?? null,
        primaryCompletionDate: row.primaryCompletionDate ?? null,
        completionDate: row.completionDate ?? null,
    };
}

// A changed study is re-delivered with these fields describing exactly what moved, so a buyer
// doesn't have to diff the row against their own last-seen copy to find out.
function changesBetween(prev, next) {
    if (!prev) return null;
    const types = [];
    const previous = {};
    for (const field of ['lastUpdatePostDate', 'overallStatus', 'enrollmentCount', 'primaryCompletionDate', 'completionDate']) {
        if (prev[field] !== undefined && prev[field] !== null && prev[field] !== next[field]) {
            types.push(field);
            previous[field] = prev[field];
        }
    }
    return types.length ? { types, previous } : null;
}

async function saveWatchRecord(status_) {
    const all = Array.from(watchSeen.entries());
    const entries = all.slice(-WATCH_KEEP);
    // An id past the record cap is not forgotten harmlessly: the next run does not find it in the
    // baseline, so the study is delivered and CHARGED again even though the buyer already paid for
    // it. The dropped end is oldest-FIRST-SEEN (re-seeing an nctId re-uses its existing Map key and
    // does not move it), so on a registry where a study keeps matching the same condition/sponsor
    // filter for years, the ids that fall off are exactly the long-lived studies that will match
    // again on the very next run. The cap itself is deliberate (KV record size budget); the bug
    // this fixes was that it applied in silence.
    baselineTruncated = all.length - entries.length;
    baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
    if (baselineTruncated > 0) {
        log.warning(
            `The baseline for "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the ${baselineTruncated} `
            + 'oldest nctId(s) were dropped and will be returned and CHARGED as new on a future run '
            + `(${baselineTruncatedTotal} dropped over the life of this label). Narrow the watch query `
            + '(conditions, interventions, sponsors, locations, overallStatus, phases, the date windows) or split '
            + 'it across several labels so each baseline stays under the cap.',
        );
    }
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
        criteria: watchCriteria,
        lastRunAt: new Date().toISOString(),
        lastRunStatus: status_,
        runCount: (watchRecord.runCount ?? 0) + 1,
        seenCount: entries.length,
        truncatedLastRun: baselineTruncated,
        truncatedTotal: baselineTruncatedTotal,
        // Compact per-entry shape (id + 5 short-keyed snapshot fields).
        seenIds: entries.map(([id, snap]) => ({
            i: id, u: snap.lastUpdatePostDate, s: snap.overallStatus, n: snap.enrollmentCount, p: snap.primaryCompletionDate, c: snap.completionDate,
        })),
    });
}

// Empty unless WATCH_KEEP actually dropped something, so it can never add noise to a healthy run.
function truncationNote() {
    if (baselineTruncated <= 0) return '';
    return ` WARNING: the baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest nctId(s) were`
        + ' dropped -- those will be delivered and charged again as "new". Narrow the query or split it across labels.';
}

if (watchMode) {
    watchStore = await Actor.openKeyValueStore(WATCH_STORE);
    const { key, fingerprint } = watchKeyFor(watchLabel, watchCriteria);
    watchKey = key;
    const existing = await watchStore.getValue(key);
    if (existing && Array.isArray(existing.seenIds)) {
        watchRecord = existing;
        // Pre-change-tracking records stored `seenIds` as a flat array of nctId strings (every
        // record predates this feature) -- those ids get a null snapshot, so `watchChanges`
        // only starts detecting drift from this run onward, never against a backlog it never
        // captured.
        for (const entry of existing.seenIds) {
            if (entry && typeof entry === 'object') {
                watchSeen.set(String(entry.i), {
                    lastUpdatePostDate: entry.u ?? null,
                    overallStatus: entry.s ?? null,
                    enrollmentCount: entry.n ?? null,
                    primaryCompletionDate: entry.p ?? null,
                    completionDate: entry.c ?? null,
                });
            } else {
                watchSeen.set(String(entry), {
                    lastUpdatePostDate: null, overallStatus: null, enrollmentCount: null, primaryCompletionDate: null, completionDate: null,
                });
            }
        }
        log.info(
            `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
            + `${watchSeen.size} already-delivered stud(y/ies). Only studies NOT in that baseline are returned and charged`
            + (watchChanges ? ', plus any already-delivered study whose status, last-update date, enrollment count or completion date changed.' : '.'),
        );
    } else {
        watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
        seeding = true;
        log.info(
            `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
            + 'It records which studies already match and returns ZERO results (you are charged nothing). Run it '
            + 'again on the same label and filters -- on a schedule, typically -- to get only what is new since now.',
        );
    }
}

// DEAD DATE BOUNDS (cycle 1584, 11th fleet instance of this class). Separate defect from the
// CHANGE-BLIND block below and gated on watchMode ALONE, not `watchMode && watchChanges`: a dead
// upper bound blinds the watch to brand-new RECORDS, which is the core job of every watch run
// whether or not change tracking is on. Every date filter here is one server-side
// `AREA[<area>]RANGE[from,to]` clause, so the registry itself stops returning the row -- there is
// no client-side field-presence gate to slip through (same shape as hacker-news-scraper's Algolia
// numericFilter, unlike ats-jobs-scraper's truthy gate).
//
// ONLY REGISTRY-EVENT dates belong here -- the date the registry did something, which for anything
// new is always "now" and never moves backwards afterwards. Measured live against the real API
// before shipping rather than pattern-matched off the previous 10 instances:
//   - firstPostedDateTo (StudyFirstPostDate): set when the record is first posted, immutable after.
//   - resultsFirstPostedDateTo (ResultsFirstPostDate): set when a results section is first posted.
//   - lastUpdatePostedDateTo (LastUpdatePostDate): an update only ever moves this LATER, so a fixed
//     upper bound defeats both new registrations and every subsequent revision. Strictest of the
//     three; it is also listed in the change-blind block below, but that one only fires when
//     watchChanges is ON, so plain watch mode was previously unwarned.
//
// STUDY-INTRINSIC dates are deliberately NOT flagged (`studyStartDateTo`,
// `primaryCompletionDateTo`, `studyCompletionDateTo`): they describe the trial's own timeline, not
// a registry event, so a record posted today can perfectly well carry a start date from years ago
// and a fixed upper bound on them still admits new rows forever. Measured 2026-10-12, not reasoned:
// of 5,660 studies first posted on/after 2026-09-01, 80 have a StartDate on/before 2020-01-01 (13
// of them first posted on/after 2026-10-01). A guard on those would be a false alarm.
// Single flat line of the schema's LITERAL input names, deliberately not assembled from the table
// below: cycle 1577's lesson is that the static check-change-blind checker can only see a guard
// whose covered inputs are spelled out as string literals next to a `watch*DateBound` identifier.
// Dynamic `.map()`-built names read as an unguarded Actor and the pass-2 hit never clears.
const watchDeadDateBoundInputs = ['firstPostedDateTo', 'resultsFirstPostedDateTo', 'lastUpdatePostedDateTo'];
const DEAD_BOUND_COPY = {
    firstPostedDateTo: ['the date a study record was FIRST POSTED to the registry',
        'a brand-new registration is first posted today, so it can never be dated on or before a cutoff already in the past'],
    resultsFirstPostedDateTo: ['the date a study\'s RESULTS were first posted',
        'a newly-posted results section is posted today, so it can never fall on or before a past cutoff'],
    lastUpdatePostedDateTo: ['the date a record was LAST UPDATED',
        'any new or freshly-revised record has a last-update date of today, so it can never fall on or before a past cutoff'],
};
const DEAD_DATE_BOUNDS = watchDeadDateBoundInputs
    .filter((name) => DATE_RE.test(String(input[name] ?? '')))
    .map((name) => [name, input[name], ...DEAD_BOUND_COPY[name]]);
const watchDeadDateBounds = watchMode ? DEAD_DATE_BOUNDS.map(([name]) => name) : [];
if (watchDeadDateBounds.length) {
    for (const [name, value, means, why] of DEAD_DATE_BOUNDS) {
        log.warning(
            `watchLabel "${watchLabel}" is combined with a fixed ${name} (${value}), an upper bound on `
            + `${means}. Because ${why}, this watch will never report a new study once the real calendar date `
            + `passes that cutoff -- and it will keep reporting a healthy "nothing new" every run while blind.`,
        );
    }
    log.warning(
        `Drop ${watchDeadDateBounds.join(' / ')} from a watched query (the matching ...From lower bound is safe to `
        + 'keep -- it only limits how far back the first baseline reaches), or remove watchLabel if you really do '
        + 'want a fixed historical window rather than an ongoing watch.',
    );
    // Honest about the one escape hatch, measured rather than asserted: these bounds blind NEW
    // registrations, but a study already inside the window that is merely revised still matches and
    // still produces a watchChanges event. Live on 2026-10-12: 2,677 studies first posted on/before
    // 2020-01-01 had an update posted on/after 2026-09-01 (62 for the results-posted equivalent).
    // So a firstPostedDateTo watch goes quiet on new trials while change events keep flowing, which
    // makes the failure even easier to mistake for a healthy watch. lastUpdatePostedDateTo has no
    // such hatch -- it blinds the revisions too.
    if (watchChanges && !watchDeadDateBounds.includes('lastUpdatePostedDateTo')) {
        log.warning(
            'Note: watchChanges events on studies ALREADY inside the window can still fire, so this run may look '
            + 'healthy. It is specifically NEW studies that can no longer appear.',
        );
    }
}

// CHANGE-BLIND FILTERS (cycle 861, ported from grants-gov-scraper cycle 860). watchChanges can
// only compare an already-delivered study against its snapshot if that study is still IN this
// run's match set -- change detection lives inside the per-row walk, so a study the query no
// longer returns is never compared and its change is never reported. That makes a filter ON A
// FIELD watchChanges TRACKS self-defeating: the very mutation the buyer is watching for (e.g.
// Recruiting -> Completed) is what removes the study from view. Unlike grants-gov, none of these
// filters is set by default here, so the buyer has to opt into the trap -- this is advisory only,
// no default-behaviour change. `lastUpdatePostedDateFrom` is deliberately NOT flagged: an update
// only ever moves lastUpdatePostDate LATER, so a lower bound can never be defeated by the change
// being watched for; `...To` can, since a fresh update can push the date past the upper bound.
const watchChangeBlindFilters = [];
if (watchMode && watchChanges) {
    if (overallStatus.length) {
        watchChangeBlindFilters.push('overallStatus (blinds an overallStatus change that moves a study OUT of the selected status(es) -- e.g. Recruiting -> Completed/Terminated)');
    }
    if (dateCriteria.lastUpdatePostedDateTo) {
        watchChangeBlindFilters.push('lastUpdatePostedDateTo (blinds a fresh update whose lastUpdatePostDate moves past this upper bound)');
    }
    if (dateCriteria.primaryCompletionDateFrom || dateCriteria.primaryCompletionDateTo) {
        watchChangeBlindFilters.push('primaryCompletionDateFrom/primaryCompletionDateTo (blinds a primaryCompletionDate revision that moves the readout date outside this window)');
    }
    if (dateCriteria.studyCompletionDateFrom || dateCriteria.studyCompletionDateTo) {
        watchChangeBlindFilters.push('studyCompletionDateFrom/studyCompletionDateTo (blinds a completionDate revision that moves the readout date outside this window)');
    }
    if (watchChangeBlindFilters.length) {
        log.warning(
            `watchChanges is ON but ${watchChangeBlindFilters.length} of this run's filter(s) narrow on a field it `
            + `tracks, so those changes can NEVER be reported -- the change itself removes the study from the `
            + `match set, and only studies still in the match set are compared against the baseline: `
            + `${watchChangeBlindFilters.join('; ')}.`,
        );
        // Deliberately a SECOND log line: the platform truncates an over-long one with
        // "[line-too-long]" (seen live on grants-gov-scraper build 0.1.36), and the half that says
        // what to do about it is the half worth keeping.
        log.warning(
            'Fix for the change-blind filter(s) above: for each field you want change alerts on, widen (or drop) the filter on THAT field for this watch '
            + 'label -- filtering your own copy of the rows afterward instead. Widening costs nothing to backfill: a '
            + 'label\'s FIRST run on a new filter set is a free baseline (0 studies charged), so studies the wider '
            + 'query newly matches land in that baseline for free and are never charged. Studies NOT in the '
            + 'baseline are still charged as new, as always. This warning is advisory -- the run continues exactly as configured.',
        );
    }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// `apiGet` returns `null` for EVERY failure shape (non-200, non-JSON body, 4 exhausted retries,
// network throw). Before cycle 646 every caller collapsed that null into "the walk is finished",
// so a 5xx on page 3 of 9 ended the run through the same `break` as a genuine last page: the run
// logged `Done. Pushed N rows` and SUCCEEDED with a third of the match set. `lastApiError` carries
// WHY the null happened so callers can tell "we reached the end" from "we stopped being answered".
// Set on every failure, cleared on every success -- always read it immediately after the call.
let lastApiError = null;
// Companion status code: lets callers tell a 400/404/422 (ClinicalTrials.gov rejecting the
// request itself -- retrying the same input fails identically) apart from a 429/5xx/network
// fault (genuinely worth retrying). Same shape as the h836 TED fix. null for network-level
// throws and the final "4 attempts exhausted" fallback, since no status code exists there.
let lastApiErrorStatus = null;
const INPUT_ERROR_STATUS = new Set([400, 404, 422]);

async function apiGet(params, { quiet = false } = {}) {
    const qs = new URLSearchParams();
    for (const [k, v] of Object.entries(params)) {
        if (Array.isArray(v)) { if (v.length) qs.set(k, v.join(',')); }
        else if (v != null && v !== '') qs.set(k, String(v));
    }
    const url = `${API}?${qs.toString()}`;
    for (let attempt = 1; attempt <= 4; attempt += 1) {
        if (!timeBudgetOk()) {
            // Deliberately silent even outside `quiet` mode: the single named 'time-budget' line
            // the callers log once is the useful signal, not one warning per in-flight request.
            // `lastApiErrorStatus = null` is load-bearing -- markIncomplete() defaults its `status`
            // param from this variable, and `seedFailureIsInputError` later tests that status
            // against INPUT_ERROR_STATUS. Leaving a stale 4xx here would make a clock-caused stop
            // advise the buyer to "fix the filter values", which is wrong and unactionable.
            timeBudgetExceeded = true;
            lastApiError = `stopped before the platform run timeout (attempt ${attempt}/4)`;
            lastApiErrorStatus = null;
            return null;
        }
        let resp;
        try {
            resp = await gotScraping({
                url,
                responseType: 'text',
                throwHttpErrors: false,
                retry: { limit: 0 },
                timeout: { request: 60000 },
                headers: { accept: 'application/json' },
            });
        } catch (err) {
            // A network-level failure (timeout, ECONNRESET, DNS) throws instead of resolving with
            // a status code — without this catch it crashes the whole run instead of retrying like
            // a 429/5xx does, even though the same backoff is exactly as valid here.
            lastApiError = `request failed: ${err.message}`;
            lastApiErrorStatus = null;
            const waitS = attempt * 10;
            if (!quiet) log.warning(`ClinicalTrials.gov API request failed (${err.message}); retrying in ${waitS}s (${attempt}/4).`);
            await sleep(Math.min(waitS * 1000, Math.max(remainingMs(), 0)));
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            lastApiError = `HTTP ${resp.statusCode}`;
            lastApiErrorStatus = resp.statusCode;
            // A server Retry-After has no upper bound of its own (a real one logged elsewhere on
            // this fleet: 3600s) -- never let it sleep past this run's own timeout.
            const waitS = Number(resp.headers['retry-after']) || attempt * 10;
            const waitMs = Math.min(waitS * 1000, Math.max(remainingMs(), 0));
            log.warning(`ClinicalTrials.gov API returned ${resp.statusCode}; retrying in ${Math.round(waitMs / 1000)}s (${attempt}/4).`);
            await sleep(waitMs);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200) {
            const detail = parsed?.errors ? JSON.stringify(parsed.errors) : String(resp.body).slice(0, 300);
            lastApiError = `HTTP ${resp.statusCode}: ${detail.slice(0, 200)}`;
            lastApiErrorStatus = resp.statusCode;
            if (!quiet) log.warning(`ClinicalTrials.gov API ${resp.statusCode}: ${detail}`);
            return null;
        }
        if (!parsed) {
            lastApiError = `non-JSON body: ${String(resp.body).slice(0, 120)}`;
            lastApiErrorStatus = null;
            if (!quiet) log.warning(`ClinicalTrials.gov returned a non-JSON body: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        lastApiError = null;
        lastApiErrorStatus = null;
        return parsed;
    }
    lastApiError = `${lastApiError ?? 'request failed'} (4 attempts exhausted)`;
    if (!quiet) log.warning('ClinicalTrials.gov API kept erroring after 4 attempts; stopping early.');
    return null;
}

// `countTotal=true` makes the API return `totalCount` -- the number of studies the REGISTRY says
// match these filters, which is the only thing a buyer can compare our row count against. Measured
// live cycle 646: `query.cond=cancer` declares 123,498. It is requested on the FIRST page only
// (verified: the key is simply absent without the flag), because a recount taken mid-walk would be
// taken against a moving index and could understate the very shortfall we are reporting.
function baseParams({ countTotal = false } = {}) {
    const p = { pageSize: MAX_PAGE_SIZE };
    if (countTotal) p.countTotal = 'true';
    if (conditions) p['query.cond'] = conditions;
    if (interventions) p['query.intr'] = interventions;
    if (sponsors) p['query.spons'] = sponsors;
    if (locations) p['query.locn'] = locations;
    if (searchQuery) p['query.term'] = searchQuery;
    if (titleOrAcronym) p['query.titles'] = titleOrAcronym;
    if (outcomeMeasure) p['query.outc'] = outcomeMeasure;
    if (overallStatus.length) p['filter.overallStatus'] = overallStatus;
    // Verified live: `filter.hasResults` is rejected as unknown; `aggFilters=results:with` is
    // the real parameter name for this. Multiple aggFilters pairs are COMMA-separated and AND-ed
    // (`docs:sap,results:with` verified live: 9,559 vs 10,597 / 18,341 for each alone).
    // Seeded with whatever a `startUrl` carried (status/phase/studyType/sex/healthy/ages/funderType
    // already stripped above when a typed input for that key is present). A typed `results`/`docs`/
    // `violation` input overwrites its own startUrl code here instead, since those three route
    // through this same Map -- the API takes the LAST value for a repeated key, not the intersection.
    // (`effectiveAggFilters` computed once, above, so this is the same Map watchCriteria fingerprints.)
    if (effectiveAggFilters.size) p.aggFilters = [...effectiveAggFilters].map(([k, v]) => `${k}:${v}`).join(',');
    // studyType/phase/sex/healthyVolunteers/date-range are AREA-scoped fields, not top-level
    // filters — combine into filter.advanced. Verified live (this cycle): AREA[Sex](FEMALE),
    // AREA[HealthyVolunteers](true) and AREA[<field>]RANGE[from,to] (MIN/MAX for an open bound)
    // all work against the real API.
    const advanced = [];
    if (studyTypes.length) advanced.push(`AREA[StudyType](${studyTypes.join(' OR ')})`);
    if (phases.length) advanced.push(`AREA[Phase](${phases.join(' OR ')})`);
    if (sex) advanced.push(`AREA[Sex](${sex})`);
    if (acceptsHealthyVolunteers) advanced.push('AREA[HealthyVolunteers](true)');
    advanced.push(...dateRanges);
    if (facilityName) advanced.push(`AREA[LocationFacility](${areaPhrase(facilityName)})`);
    if (leadSponsorName) advanced.push(`AREA[LeadSponsorName](${areaPhrase(leadSponsorName)})`);
    if (ageRangeFromYears !== null) advanced.push(`AREA[MinimumAge]RANGE[${ageRangeFromYears} ${ageRangeFromUnit},MAX]`);
    if (ageRangeToYears !== null) advanced.push(`AREA[MaximumAge]RANGE[MIN,${ageRangeToYears} ${ageRangeToUnit}]`);
    if (funderTypes.length) advanced.push(`AREA[LeadSponsorClass](${funderTypes.join(' OR ')})`);
    if (ageGroups.length) advanced.push(`AREA[StdAge](${ageGroups.join(' OR ')})`);
    if (advanced.length) p['filter.advanced'] = advanced.join(' AND ');
    if (sortBy) p.sort = sortBy;
    return p;
}

// Verified live: `filter.ids=NCT1,NCT2,...` works, but if ANY id in the batch is malformed or
// doesn't exist, ClinicalTrials.gov 400s the WHOLE request (not a partial/ignore-bad-ones
// response) — a single typo silently makes an otherwise-correct batch return zero rows unless
// handled explicitly. Bisect on failure so one bad id can't take out an entire good batch.
// nctIds deliberately does NOT combine with the search filters below (conditions/interventions/
// sponsors/locations/searchQuery/overallStatus/studyTypes/phases/hasResultsOnly): `conditions`
// carries a schema `default` of "cancer" that Apify applies server-side to any input missing the
// field (verified cycle 96/121), so an API caller who sends only `nctIds` would otherwise get an
// invisible `AND query.cond=cancer` and silently lose every non-cancer trial they asked for.
//
// Measured live cycle 646, and it changes what the two outcomes MEAN. A well-formed id the
// registry does not hold (`NCT99999999`) comes back **200 with an empty `studies` array**, not a
// 400 — only a MALFORMED id (`NOTANID`) 400s. So before this cycle: (a) a well-formed unknown id
// produced no row and no mention anywhere, because the success branch returned `notFound: []` and
// nobody diffed the request against the response; and (b) the only ids that ever reached the old
// `notFound` list were malformed ones and ones whose request FAILED — yet the run reported all of
// them as "not found on ClinicalTrials.gov", a claim about the registry that a timeout cannot
// support. The three outcomes are now kept apart: `notFound` (asked, answered, absent),
// `malformed` (the registry rejected the id itself) and `failed` (we never got an answer).
async function resolveIdsChunk(ids) {
    const params = { 'filter.ids': ids, pageSize: Math.min(MAX_PAGE_SIZE, Math.max(ids.length, 1)) };
    const page = await apiGet(params, { quiet: ids.length > 1 });
    if (page) {
        const studies = listOf(page.studies);
        const got = new Set(studies.map((s) => s.protocolSection?.identificationModule?.nctId).filter(Boolean));
        // Case-insensitive: the API accepts lowercase ids and echoes them back upper-cased.
        const gotUpper = new Set([...got].map((s) => s.toUpperCase()));
        return {
            studies,
            notFound: ids.filter((id) => !gotUpper.has(String(id).toUpperCase())),
            malformed: [],
            failed: [],
        };
    }
    if (ids.length === 1) {
        const isBadId = /^HTTP 400\b/.test(String(lastApiError));
        return isBadId
            ? { studies: [], notFound: [], malformed: ids, failed: [] }
            : { studies: [], notFound: [], malformed: [], failed: ids };
    }
    // Out of clock: splitting would recurse down to one doomed apiGet per id (each now returning
    // instantly), producing nothing but noise. Report them all as never-answered, which is what
    // they are, and let the caller's `failedIds` branch name the cause once.
    if (timeBudgetExceeded) return { studies: [], notFound: [], malformed: [], failed: ids };
    const mid = Math.ceil(ids.length / 2);
    const [a, b] = await Promise.all([resolveIdsChunk(ids.slice(0, mid)), resolveIdsChunk(ids.slice(mid))]);
    return {
        studies: [...a.studies, ...b.studies],
        notFound: [...a.notFound, ...b.notFound],
        malformed: [...a.malformed, ...b.malformed],
        failed: [...a.failed, ...b.failed],
    };
}

const listOf = (v) => (Array.isArray(v) ? v.filter(Boolean) : []);

// eligibilityCriteria is the only field in this API confirmed to carry undecoded HTML entities
// (measured live: 7 hits / 100 studies sampled with this Actor's own filters, kinds &gt;/&lt;/
// &amp;/&#39; — e.g. "Age &gt; 18"; zero raw tags, so this is a decode fix, not a strip fix, same
// class of bug as grants-gov-scraper cycle 556). All other free-text fields (briefSummary,
// outcome measure/description, titles) came back clean on the same 100-study sample.
// cycle 1607: a single decode pass only resolves one layer of encoding (grants-gov cycle 1606
// shipped double-encoded `&amp;rsquo;`, which one pass turns into a leftover `&rsquo;`) — no
// double-encoded row has been observed here yet, but nothing rules one out, so decode to a
// fixpoint defensively, same fix shape as grants-gov.
const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ' };
const decodeEntitiesOnce = (s) => String(s).replace(/&(#x[0-9a-fA-F]+|#\d+|[a-zA-Z][a-zA-Z0-9]{1,9});/g, (m, e) => {
    if (e[0] === '#') {
        const cp = e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
        return Number.isFinite(cp) && cp > 0 && cp <= 0x10ffff ? String.fromCodePoint(cp) : m;
    }
    const key = e.toLowerCase();
    return Object.prototype.hasOwnProperty.call(ENTITIES, key) ? ENTITIES[key] : m; // unknown entity: leave verbatim
});
const decodeEntities = (s) => {
    let prev = String(s);
    for (let i = 0; i < 5; i += 1) {
        const next = decodeEntitiesOnce(prev);
        if (next === prev) break;
        prev = next;
    }
    return prev;
};

// Every field/location contact carries a real person's name, phone and/or personal email
// (verified live, incl. an @gmail.com in the sample) — CLAUDE.md rule 1 bans shipping PII, so
// contacts[] is deliberately never read. Location rows keep only facility/geo/status data.
const outcomeOf = (o) => ({
    measure: o.measure ?? null,
    timeFrame: o.timeFrame ?? null,
    description: o.description ?? null,
});

// WHY a study stopped, classified from the sponsor's free-text `whyStopped` (shipped raw,
// cycle 2290) into a fixed set of categories. Same shape as fda-recall-scraper's
// `ROOT_CAUSE_RULES` (cycle 2288): an ordered, first-match-wins list of published regexes, no
// model call, no network, deterministic (CLAUDE.md rule 2) -- the same text always yields the
// same category. `datalayer/clinical-trials-failure-intel` does this classification; we did
// not until this field shipped.
//
// MEASURED on two independent live samples pulled 2026-10-26 (TERMINATED/WITHDRAWN/SUSPENDED
// studies, 100 per status via the ClinicalTrials.gov API v2, paginated with `pageToken` so the
// two samples share no rows): 88.5% classified on the 269-row tuning sample (after one
// generalization pass reading the holdout misses -- the same "read the misses, fix the
// one-off rules" process fda-recall used), and **82.2% on a 276-row holdout never used for
// tuning** (skip tuning rows via pageToken). Report the holdout number, not the tuned one.
// `whyStopped` text is far more free-form than FDA's recall reasons (many one-off sponsor
// sentences), which is why this holdout rate is lower than fda-recall's 96.3% -- an honest
// reflection of the source text, not a weaker rule set.
//
// RE-MEASURED cycle 2296 on the same two samples (the API returns the same first two pages per
// status, so both re-pulled identically: 269 tuning / 276 holdout, 0 overlap) after splitting
// `device_or_technical_issue` out of `drug_or_supply_issue`: coverage is UNCHANGED at 88.5%
// tuning / 82.2% holdout (the split relabels rows, it does not add matches), and exactly the 7
// intended equipment/technical rows moved category -- no collateral relabelling anywhere else.
const WHY_STOPPED_RULES = [
    ['safety_or_adverse_event', /safety\s+(?:concern|issue|event|signal|question|result)|adverse\s+(?:event|reaction|effect)|unacceptable\s+toxicity|\btoxicity\b|risk[- ]benefit|unfavorable\s+risk|clinical\s+hold|severe\s+adverse|dose[- ]limiting\s+toxicity|\bdlt\b|data\s+safety\s+monitoring\s+board|\bdsmb\b|\bdsmc\b|ind[ei]pendent\s+(?:data\s+)?monitoring\s+committee|non-?specific\s+binding/i],
    ['lack_of_efficacy', /futility|lack\s+of\s+efficacy|no\s+efficacy|poor\s+efficacy|low\s+cure\s+rate|insufficient\s+efficacy|(?:did\s+not|didn['’]?t)\s+meet[^.]{0,60}(?:efficacy|progression-free|primary\s+(?:endpoint|outcome)|pre-?specified)|fail(?:ed|ure)\s+to\s+(?:meet|demonstrate)[^.]{0,40}(?:efficacy|endpoint|superiority|benefit)/i],
    // Equipment/instrument malfunction and bare "technical problem/issue" text. Split out of
    // `drug_or_supply_issue` in cycle 2296: a varied-input test (c2295) found "technical problem
    // in the laser device" labelled a drug-supply issue, and reading every row in that category
    // across both measured samples showed 7 of 22 were equipment/technical failures, not study
    // material availability -- a third of the category was wrong, not one anecdote. Ordered
    // BEFORE `drug_or_supply_issue` so an equipment failure wins over the supply reading, but
    // deliberately does NOT match a bare "device" noun, so genuine supply text ("study device no
    // longer available") still classifies as `drug_or_supply_issue`.
    ['device_or_technical_issue', /device[- ]related\s+(?:issue|problem|failure)|equipment\s+(?:failure|issue|problem|malfunction|breakdown)|technical\s+(?:difficult\w*|problem|issue|failure|support|malfunction)|malfunction(?:ing)?\s+of\s+(?:the\s+)?(?:device|equipment|machine|instrument|scanner|system)|(?:device|machine|instrument|scanner|laser|equipment)\s+(?:malfunction|broke|broken|failure)|(?:machine|instrument|scanner|device)\s+(?:is\s+)?(?:out\s+of\s+order|no\s+longer\s+works?)/i],
    ['drug_or_supply_issue', /(?:drug|device|product|reagents?|isotope|supply|material)[^.]{0,15}no\s+longer\s+available|no\s+longer\s+available\s+from|availability\s+of[^.]{0,40}reagent|reagents?\s+(?:availability|shortage)|manufacturing\s+process|drug\s+(?:supply|shortage)|isotope[^.]{0,30}available|study\s+drug\s+expired|expired[^.]{0,20}study\s+drug|investigational\s+product|production\s+(?:not\s+available|issue)|concerns?\s+(?:related\s+to|about)\s+(?:the\s+)?study\s+drug|no\s+longer\s+supply|withdrew\s+(?:their\s+)?(?:interest|support)|withdrawal\s+of\s+support|not\s+(?:currently\s+)?supporting\s+research|unable\s+to\s+secure\s+(?:study\s+)?medication|study\s+medication\s+supply|expiry\s+of\s+study\s+drug|no\s+replacement\s+available/i],
    ['covid_19', /covid|corona\s*virus|pandemic/i],
    ['low_enrollment', /enroll?ment|enroll?(?:ed|ing)?|recruit|accrual|accru\w*|lack\s+of\s+patients|insufficient\s+(?:number\s+of\s+)?patients|inadequate\s+(?:number\s+of\s+)?patients|no\s+eligible\s+patient|sample\s+size[^.]{0,25}not\s+(?:achieved|met|reached|completed)|lack\s+of\s+inclusion|inclusion\w*\s+not\s+reached|target\s+number\s+of\s+(?:patients|inclusion)|expected\s+number\s+of\s+patients|reduction\s+in\s+(?:the\s+)?number\s+of\s+(?:cases|patients)|difficulty[^.]{0,20}including\s+participants|lack\s+of\s+potential\s+participants/i],
    ['administrative_or_sponsor_decision', /\birb\b|ethic(?:s|al)\s+committee|regulatory|protocol[^.]{0,25}modif\w*|protocol\s+amendment|pending\s+amendment|duplicat\w*\s+(?:record|entry|registration)|never\s+(?:started|initiated)|not\s+(?:started|initiated)|n['’]?t\s+started|did\s+not\s+initiate|not\s+(?:being\s+)?pursued|sponsor\w*\s+(?:decision|decid\w*|withdr\w*|cancel\w*|discontinu\w*|want\w*|reasons?|(?:has\s+)?changed)|cancel(?:ed|led)\s+by\s+(?:the\s+)?sponsor|site\s+decid\w*|\bpi\s+decis\w*\b|\bpi\s+decid\w*\b|mutual\s+agreement|interim\s+analysis|government\s+(?:executive\s+)?order|government\s+oversight|\bfwa\b\s+restriction|\bhhs\b|\bohrp\b|administrat|for\s+sponsor\s+reasons|lack\s+of\s+feasibility|not\s+feasible|unfeasible|infeasib|\bon\s+hold\b|put\s+on\s+hold|change\s+in\s+study\s+design|change\s+in\s+(?:hospital\s+)?protocol|protocol\s+will\s+be\s+changed/i],
    ['funding_or_business', /\bfund(?:ing|ed|s)?\b|financ|budget(?:ary)?|business\s+(?:decision|reason)|strategic|portfolio|commercial\s+reason|lack\s+of\s+resources|research\s+priorit|company\s+(?:decision|strategy)|strategy\s+adjust|grant\s+(?:application|rejected|denied)|program\s+discontinu|bankrupt\w*|acqui\w*|wind\s+down\s+operations|ended\s+operations|commercializ\w*|development\s+strategy/i],
    ['logistical_or_operational', /staff(?:ing)?|personnel|\bpi\s+(?:is\s+)?(?:left|leaving|request|resign\w*|return\w*)\b|terminated\s+by\s+pi|withdrawn\s+by\s+(?:principal\s+)?investigator|investigator\s+(?:is\s+)?left|principal\s+investigator\s+(?:is\s+)?left|investigator'?s?\s+(?:other\s+)?responsibilit|insufficient\s+time|site\s+(?:closure|closed|ceased)|operational|organi[sz]ation\w*|relocat|institution|graduated|retired|unable\s+to\s+complete|inability\s+to\s+complete|not\s+able\s+to\s+(?:be\s+)?continu\w*|research(?:er)?\s+(?:is\s+)?unable\s+to\s+continue|research(?:er)?\s+in\s+charge\s+(?:has\s+)?left|left\s+the\s+affiliation|dissolution\s+of\s+(?:the\s+)?(?:research\s+)?team|logistic\w*|thesis/i],
];
function classifyStopReason(why) {
    if (!why || !String(why).trim()) return { stopReason: null, stopReasons: [] };
    const text = String(why);
    const hits = WHY_STOPPED_RULES.filter(([, re]) => re.test(text)).map(([c]) => c);
    if (hits.length === 0) return { stopReason: 'other', stopReasons: ['other'] };
    return { stopReason: hits[0], stopReasons: hits };
}

function normalizeStudy(study) {
    const p = study.protocolSection ?? {};
    const id = p.identificationModule ?? {};
    const status = p.statusModule ?? {};
    const sponsor = p.sponsorCollaboratorsModule ?? {};
    const design = p.designModule ?? {};
    const desc = p.descriptionModule ?? {};
    const cond = p.conditionsModule ?? {};
    const arms = p.armsInterventionsModule ?? {};
    const out = p.outcomesModule ?? {};
    const elig = p.eligibilityModule ?? {};
    const locs = listOf(p.contactsLocationsModule?.locations);

    const facilities = locs.map((l) => ({
        facility: l.facility ?? null,
        status: l.status ?? null,
        city: l.city ?? null,
        state: l.state ?? null,
        country: l.country ?? null,
        lat: l.geoPoint?.lat ?? null,
        lon: l.geoPoint?.lon ?? null,
    }));

    return {
        nctId: id.nctId ?? null,
        briefTitle: id.briefTitle ?? null,
        officialTitle: id.officialTitle ?? null,
        acronym: id.acronym ?? null,
        overallStatus: status.overallStatus ?? null,
        // Only the registry sets this -- almost always on TERMINATED/WITHDRAWN/SUSPENDED studies,
        // null on everything else (verified live 2026-10-26, 50-row samples: 0/50 RECRUITING,
        // 0/50 COMPLETED, 43/50 TERMINATED, 46/50 WITHDRAWN, 45/50 SUSPENDED carry a value).
        // Sponsor's own free text, shipped raw and undecoded on purpose -- same "source text, not
        // a heuristic label" call as eligibilityCriteria above.
        whyStopped: status.whyStopped ?? null,
        // WHY the study stopped, classified from whyStopped above -- see WHY_STOPPED_RULES.
        ...(includeStopReason ? classifyStopReason(status.whyStopped) : { stopReason: null, stopReasons: [] }),
        studyType: design.studyType ?? null,
        // Populated on ~81% of studies (measured live sample of 50) — absent for many
        // observational studies. Never advertised as guaranteed.
        phases: listOf(design.phases),
        enrollmentCount: design.enrollmentInfo?.count ?? null,
        // ACTUAL vs ESTIMATED — enrollmentCount alone is ambiguous, and an "estimated" count on a
        // not-yet-completed trial is a target, not a headcount. Present on 20/20 of a live sample.
        enrollmentType: design.enrollmentInfo?.type ?? null,
        startDate: status.startDateStruct?.date ?? null,
        primaryCompletionDate: status.primaryCompletionDateStruct?.date ?? null,
        completionDate: status.completionDateStruct?.date ?? null,
        studyFirstPostDate: status.studyFirstPostDateStruct?.date ?? null,
        // Only set once results are posted (4/20 on a live sample) — this is the field the
        // resultsFirstPostedDateFrom/To filters range over, so a buyer filtering on it could not
        // previously see the value they filtered by.
        resultsFirstPostDate: status.resultsFirstPostDateStruct?.date ?? null,
        lastUpdatePostDate: status.lastUpdatePostDateStruct?.date ?? null,
        leadSponsor: sponsor.leadSponsor?.name ?? null,
        leadSponsorClass: sponsor.leadSponsor?.class ?? null,
        // Populated on ~24% of studies (measured live sample of 50) — most trials have none.
        collaborators: listOf(sponsor.collaborators).map((c) => c.name).filter(Boolean),
        conditions: listOf(cond.conditions),
        keywords: listOf(cond.keywords),
        interventions: listOf(arms.interventions).map((i) => ({ type: i.type ?? null, name: i.name ?? null })),
        // What the trial actually measures. The `outcomeMeasure` input already searches these
        // (query.outc), so until now a buyer could filter on an outcome and never see which one
        // matched. timeFrame is kept because "6-month HbA1c" and "5-year HbA1c" are different
        // trials to anyone screening endpoints. Primary present on 19/20, secondary on 14/20
        // of a live sample; both are [] when the study declares none.
        // `description` is included because query.outc searches it too, not just `measure`:
        // verified live this cycle, 2 of 8 hits for outcomeMeasure="HbA1c" matched ONLY in the
        // description, so dropping it would leave those rows looking like false positives.
        // Present on 132/170 outcomes sampled, median 114 chars — cheap.
        primaryOutcomes: listOf(out.primaryOutcomes).map(outcomeOf),
        secondaryOutcomes: listOf(out.secondaryOutcomes).map(outcomeOf),
        briefSummary: desc.briefSummary ?? null,
        sex: elig.sex ?? null,
        minimumAge: elig.minimumAge ?? null,
        // Populated on ~48% of studies (measured live sample of 50) — many trials have no
        // upper age bound.
        maximumAge: elig.maximumAge ?? null,
        healthyVolunteers: typeof elig.healthyVolunteers === 'boolean' ? elig.healthyVolunteers : null,
        // The registry's own CHILD/ADULT/OLDER_ADULT buckets — the exact vocabulary the
        // `ageGroups` input filters on, so the filtered value is now visible on the row.
        standardAges: listOf(elig.stdAges),
        // Free text, as the registry publishes it (median ~1.3 KB, max ~13 KB on a live sample).
        // Deliberately NOT split into inclusion/exclusion: that split is a heuristic on prose with
        // no fixed format, and mislabelling an exclusion criterion as an inclusion one is exactly
        // the error a trial-screening buyer cannot afford. Ship the source text instead.
        eligibilityCriteria: elig.eligibilityCriteria ? decodeEntities(elig.eligibilityCriteria) : null,
        hasResults: study.hasResults === true,
        locationCount: facilities.length,
        // Site facility/city/state/country/geo only — no contact person, phone or email, ever.
        locations: facilities,
        studyUrl: id.nctId ? `https://clinicaltrials.gov/study/${id.nctId}` : null,
    };
}

// ---------------------------------------------------------------------------
// Machine-readable completeness (cycle 646). 100 rows against a registry that declares 123,498
// matches reads, in the dataset, exactly like a complete result set -- and the dataset is the only
// surface a pipeline actually parses. Prose in the log does not reach it. Same design as
// fda-recall-scraper / grants-gov-scraper / app-store-reviews-scraper: a RUN_SUMMARY key-value
// record (readable with no webhook configured) plus the same object on the webhook payload.
let declaredMatches = null;     // registry's own totalCount; null = "not asked / never answered", NEVER 0
const notFoundIds = [];         // asked, answered, absent from the registry
const malformedIds = [];        // the registry rejected the id itself (HTTP 400)
const failedIds = [];           // never answered -- says NOTHING about whether the study exists
const notReachedIds = [];       // never requested, because the run stopped first
let complete = true;
let incompleteReason = null;
let incompleteDetail = null;
let incompleteStatus = null;

// First cause wins: a walk that stopped because the API stopped answering, and THEN also hit
// maxResults, must keep reporting the upstream failure -- that is the cause the buyer can act on.
// `status` defaults to whatever `lastApiErrorStatus` was AT THE MOMENT markIncomplete is called
// (JS evaluates default params at call time), so a later successful call elsewhere can't clobber it.
function markIncomplete(reason, detail = null, status = lastApiErrorStatus) {
    if (!complete) return;
    complete = false;
    incompleteReason = reason;
    incompleteDetail = detail;
    incompleteStatus = status;
}

let pushed = 0;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item) {
    if (isPPE) {
        const r = await Actor.charge({ eventName: 'result', count: 1 });
        if (r.chargedCount === 0) { markIncomplete('charge-limit'); return false; }
        await Actor.pushData(item); pushed += 1;
        if (r.eventChargeLimitReached) markIncomplete('charge-limit');
        else if (pushed >= maxResults) markIncomplete('max-results', `maxResults=${maxResults}`);
        return !r.eventChargeLimitReached && pushed < maxResults;
    }
    await Actor.pushData(item); pushed += 1;
    if (pushed >= maxResults) markIncomplete('max-results', `maxResults=${maxResults}`);
    return pushed < maxResults;
}

log.info(nctIds.length
    ? `ClinicalTrials.gov: direct-lookup mode, nctIds=[${nctIds.join(',')}] (other search filters ignored) `
      + `rowsPerStudy=${rowsPerStudy} maxResults=${maxResults}`
    : `ClinicalTrials.gov: conditions="${conditions}" interventions="${interventions}" sponsors="${sponsors}" `
      + `locations="${locations}" searchQuery="${searchQuery}" overallStatus=[${overallStatus.join(',')}] `
      + `studyTypes=[${studyTypes.join(',')}] phases=[${phases.join(',')}] hasResultsOnly=${hasResultsOnly} `
      + `sex="${sex}" acceptsHealthyVolunteers=${acceptsHealthyVolunteers} `
      + `lastUpdatePostedDateFrom="${lastUpdatePostedDateFrom}" lastUpdatePostedDateTo="${lastUpdatePostedDateTo}" `
      + `ageRangeFrom=${ageRangeFromYears === null ? 'null' : `${ageRangeFromYears} ${ageRangeFromUnit}`} `
      + `ageRangeTo=${ageRangeToYears === null ? 'null' : `${ageRangeToYears} ${ageRangeToUnit}`} funderTypes=[${funderTypes.join(',')}] `
      + `titleOrAcronym="${titleOrAcronym}" outcomeMeasure="${outcomeMeasure}" sortBy="${sortBy}" `
      + `facilityName="${facilityName}" leadSponsorName="${leadSponsorName}" `
      + `dateRanges=[${dateRanges.join(' AND ')}] `
      + `rowsPerStudy=${rowsPerStudy} maxResults=${maxResults}`
      + (watchMode ? ` watchLabel="${watchLabel}" watchChanges=${watchChanges}` : ''));

let scanned = 0;
let pages = 0;
let keepGoing = true;
let skippedSeen = 0;

// Seeding only needs ids, so it walks the search with the exact same `baseParams()`/`apiGet()`
// pagination the real run below uses -- they can never page the underlying API differently.
// `baseParams()` always requests `pageSize: MAX_PAGE_SIZE` (1000) regardless of `maxResults`, so
// (unlike federal-register-scraper cycle 297 / fda-recall-scraper cycle 299) there is no separate
// small-page-size trap to work around here; the only thing this function does differently from
// the real run is not stop early at `maxResults` -- a baseline that stopped early would report
// every study past the stopping point as "new" on the first incremental run.
async function seedBaseline() {
    let pageToken = null;
    for (;;) {
        const params = baseParams({ countTotal: pages === 0 });
        if (pageToken) params.pageToken = pageToken;
        const page = await apiGet(params);
        if (!page) {
            // The over-charge shape, 6th appearance across the fleet (h255/h264/h266/h272/h273).
            // A failed page here silently SHORTENS the baseline, and every study past the failure
            // point is then "new" on the next incremental run -- so the buyer is charged for rows
            // they already had. Loud, named, and recorded in RUN_SUMMARY.
            markIncomplete(failureReason('search-request-failed'), lastApiError);
            log.warning(
                `Baseline seed for watch label "${watchLabel}" stopped early: ${lastApiError}. The baseline is `
                + `INCOMPLETE (${watchSeen.size} recorded), so the next incremental run would deliver -- and `
                + 'CHARGE FOR -- studies past that point as if they were new. Re-run the seed before scheduling.',
            );
            break;
        }
        if (pages === 0 && Number.isFinite(page.totalCount)) declaredMatches = page.totalCount;
        const studies = listOf(page.studies);
        if (!studies.length) break;
        pages += 1;
        for (const study of studies) {
            scanned += 1;
            const nctId = study.protocolSection?.identificationModule?.nctId ?? null;
            if (nctId) watchSeen.set(nctId, snapshotOf(normalizeStudy(study)));
            if (watchSeen.size >= SEED_CAP) {
                // Measured live cycle 646 (unlike hacker-news-scraper's dead cap, h272): the v2 API
                // serves nextPageToken indefinitely at pageSize=1000 and `query.cond=cancer` alone
                // declares 123,498 matches, so this cap is reachable and this warning can fire.
                markIncomplete('seed-cap', `SEED_CAP=${SEED_CAP}`);
                log.warning(
                    `Watch label "${watchLabel}" seed hit the ${SEED_CAP}-study cap before scanning the whole `
                    + 'match set. Narrow the query (fewer conditions/locations, a shorter date window) so the '
                    + 'whole result set fits, or the first incremental run will report studies past the cap as new.',
                );
                log.info(`Baseline walk: ${watchSeen.size} stud(y/ies) recorded.`);
                return;
            }
        }
        pageToken = page.nextPageToken ?? null;
        if (!pageToken) break;
    }
    log.info(`Baseline walk: ${watchSeen.size} stud(y/ies) recorded.`);
}

async function emitStudy(row) {
    scanned += 1;
    if (rowsPerStudy === 'site') {
        const sites = row.locations.length ? row.locations : [null];
        for (const site of sites) {
            const { locations: _drop, locationCount: _drop2, ...studyFields } = row;
            keepGoing = await pushResult({ ...studyFields, site });
            if (!keepGoing) return;
        }
    } else {
        keepGoing = await pushResult(row);
    }
}

if (nctIds.length) {
    // Direct-lookup mode: fetch specific trials by NCT id (what most competitor Actors call
    // "search by direct URL"). Exclusive of the search filters below — see the note on
    // resolveIdsChunk for why they are not ANDed in here.
    const CHUNK = 500; // keeps each top-level request well under MAX_PAGE_SIZE / URL-length limits
    let i = 0;
    for (; i < nctIds.length && keepGoing; i += CHUNK) {
        const r = await resolveIdsChunk(nctIds.slice(i, i + CHUNK));
        notFoundIds.push(...r.notFound);
        malformedIds.push(...r.malformed);
        failedIds.push(...r.failed);
        pages += 1;
        for (const study of r.studies) {
            await emitStudy(normalizeStudy(study));
            if (!keepGoing) break;
        }
    }
    // Ids past an early stop were never asked about at all. Their ABSENCE from every list would
    // read as "we checked and there was nothing" -- so they are written down explicitly.
    notReachedIds.push(...nctIds.slice(Math.min(i, nctIds.length)));
    // `declaredMatches` in direct-lookup mode is the number of ids the buyer asked for; the
    // registry has no separate total to declare here.
    declaredMatches = nctIds.length;
    if (notFoundIds.length) {
        log.warning(`${notFoundIds.length} of ${nctIds.length} nctIds are not in the ClinicalTrials.gov registry: ${notFoundIds.join(', ')}`);
    }
    if (malformedIds.length) {
        log.warning(`${malformedIds.length} nctId(s) were rejected by ClinicalTrials.gov as malformed: ${malformedIds.join(', ')}`);
    }
    if (failedIds.length) {
        // Deliberately NOT folded into notFound: a failed request cannot support the claim that a
        // study is absent from the registry.
        markIncomplete(failureReason('lookup-request-failed'), lastApiError);
        log.warning(
            `${failedIds.length} nctId(s) could not be checked -- ClinicalTrials.gov never answered for them `
            + `(${lastApiError}): ${failedIds.join(', ')}. They are NOT known to be missing; re-run for these ids.`,
        );
    }
    if (notReachedIds.length) markIncomplete('max-results', `${notReachedIds.length} id(s) never requested`);
} else if (watchMode && seeding) {
    await seedBaseline();
} else {
    // Fleet-wide pattern (federal-register-scraper's `seen`, court-records-scraper's
    // `seenIdsThisRun`): a within-run duplicate guard, independent of watchMode. `sortBy` can be
    // set to `LastUpdatePostDate:desc` (SORT_VALUES above), and ClinicalTrials.gov re-indexes on
    // its own daily cadence -- a study whose lastUpdatePostDate ticks over to "today" mid-walk can
    // jump to the front of that sort order between two of this run's own page fetches, which
    // shifts the whole cursor and can hand back a study this run already paged past and paid for.
    // This is PPE (credits_per_result:1), so a repeat is a real double charge, not just a
    // duplicate row. A plain default-sort walk (verified live: two fresh fetches of the same
    // query, no token, returned byte-identical order) is effectively immune, but the walk cannot
    // tell from here which sort the buyer picked, so the guard applies unconditionally. (cycle 2318)
    const seen = new Set();
    let pageToken = null;
    while (keepGoing) {
        const params = baseParams({ countTotal: pages === 0 });
        if (pageToken) params.pageToken = pageToken;
        const page = await apiGet(params);
        if (!page) {
            markIncomplete(failureReason('search-request-failed'), lastApiError);
            log.warning(
                `Paging stopped early after ${pages} page(s): ${lastApiError}. The result set is INCOMPLETE -- `
                + 'this run returned only what was fetched before the failure. See RUN_SUMMARY.',
            );
            break;
        }
        if (pages === 0 && Number.isFinite(page.totalCount)) declaredMatches = page.totalCount;
        const studies = listOf(page.studies);
        if (!studies.length) {
            // A 200 with zero studies AND a nextPageToken still in hand is not an ending we can
            // explain, so it is written down rather than read as "that was everything".
            if (pageToken) markIncomplete('empty-page-with-token', `after ${pages} page(s)`);
            break;
        }
        pages += 1;

        for (const study of studies) {
            const nctId = study.protocolSection?.identificationModule?.nctId ?? null;
            if (nctId) {
                if (seen.has(nctId)) { scanned += 1; continue; }
                seen.add(nctId);
            }
            if (watchMode && nctId && watchSeen.has(nctId)) {
                // Already delivered under this watch label. Normally dropped before any charge,
                // so a study is never paid for twice -- UNLESS watchChanges is on and its
                // snapshot drifted since we last saw it, in which case it is re-delivered
                // (charged like a new row, exploded per-site same as any other row if
                // rowsPerStudy="site") tagged with exactly what changed.
                const row = normalizeStudy(study);
                const nextSnap = snapshotOf(row);
                const change = watchChanges ? changesBetween(watchSeen.get(nctId), nextSnap) : null;
                if (!change) {
                    // Snapshot kept current either way, so enabling the flag later detects only
                    // drift from that point, not a backlog since the baseline.
                    scanned += 1;
                    watchSeen.set(nctId, nextSnap);
                    skippedSeen += 1;
                    continue;
                }
                const before = pushed;
                await emitStudy({ ...row, _watchChangeType: change.types, _watchPrevious: change.previous });
                if (pushed > before) { watchSeen.set(nctId, nextSnap); changedCount += 1; }
                if (!keepGoing) break;
                continue;
            }
            const before = pushed;
            const row = normalizeStudy(study);
            await emitStudy(row);
            // Recorded as delivered only after the charge actually succeeded -- anything dropped
            // by maxResults or a charge limit stays "new" for the next run.
            if (watchMode && nctId && pushed > before) watchSeen.set(nctId, snapshotOf(row));
            if (!keepGoing) break;
        }

        pageToken = page.nextPageToken ?? null;
        if (!pageToken) break;
    }
}

// A failed seed walk (markIncomplete('search-request-failed', ...)) silently SHORTENS the
// baseline if saved anyway -- every study past the failure point then reads as "new" on the
// first incremental run and gets charged for again. A seed charges nothing, so re-seeding later
// is free; there is nothing lost by not persisting here. Deliberately NOT gated on 'seed-cap':
// that is the buyer's query being too broad, is reported in RUN_SUMMARY and the status message,
// and a capped baseline is still strictly better than none. Same policy as fda-recall-scraper (h289).
// 'time-budget' belongs here for the same reason: a seed walk the clock cut short is just as
// partial as one the API cut short, and saving it would re-bill the buyer for everything past
// the cutoff. (cycle 1736)
const SEED_UPSTREAM_FAILURES = new Set(['search-request-failed', 'time-budget']);
const seedFailure = seeding && incompleteReason && SEED_UPSTREAM_FAILURES.has(incompleteReason)
    ? incompleteDetail : null;
const seedFailureIsInputError = seedFailure != null && INPUT_ERROR_STATUS.has(incompleteStatus);
// Three causes, three different things the buyer has to DO about it. Telling someone whose seed
// ran out of clock to "re-run once ClinicalTrials.gov is answering again" sends them to wait on a
// service that was never down -- the same mis-advice the reason-name fix above removes from
// RUN_SUMMARY, so it is removed from the two buyer-facing messages too. (cycle 1736)
const seedFailureIsTimeBudget = seedFailure != null && incompleteReason === 'time-budget';
const seedFailureAdvice = seedFailureIsInputError
    ? 'This is ClinicalTrials.gov rejecting the input itself -- fix the filter values and re-run.'
    : seedFailureIsTimeBudget
        ? 'This run ran out of time, not out of data -- raise the Actor run timeout, or narrow the query '
            + '(fewer conditions/locations, a shorter date window), then re-run the same label.'
        : 'Re-run the same label and filters once ClinicalTrials.gov is answering again.';

if (watchMode && seedFailure) {
    log.warning(
        `Baseline walk for watch label "${watchLabel}" was cut short (${seedFailure}), so NO baseline was saved. `
        + 'A partial baseline would have caused every study past the stopping point to be delivered and charged '
        + `as "new" on your next run. ${seedFailureAdvice}`,
    );
} else if (watchMode) {
    await saveWatchRecord(seeding ? 'seeded' : 'incremental');
    if (seeding) {
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} stud(y/ies) recorded as `
            + 'already-seen, 0 results returned, 0 charged. The next run on this label and these filters '
            + `returns only new stud(y/ies)${watchChanges ? ' or ones whose status/last-update/enrollment/completion date changed' : ''}.`,
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed} new/changed stud(y/ies) since the last run (${skippedSeen} `
            + `unchanged already-delivered stud(y/ies) skipped, uncharged`
            + (watchChanges ? `, ${changedCount} of the pushed re-delivered for a change` : '')
            + `); baseline now holds ${watchSeen.size}.`,
        );
    }
}

// Apify truncates a run status message at 500 characters, silently, cutting from the end --
// measured live on this Actor (`2KyoZrB1CUMjk6kqc`, the plain-no-match message cut mid-word at
// exactly 500, losing cause (3)). Same fleet-wide defect closed on grants-gov-scraper (0.1.67)
// and fda-recall-scraper (0.1.68); applied here with the same shape, cycle 1762.
const STATUS_MESSAGE_MAX = 500;
const clampStatusMessage = (msg) => {
    if (msg.length <= STATUS_MESSAGE_MAX) return msg;
    const cut = msg.slice(0, STATUS_MESSAGE_MAX - 4);
    const lastSpace = cut.lastIndexOf(' ');
    return `${(lastSpace > 0 ? cut.slice(0, lastSpace) : cut).trimEnd()} ...`;
};

// Direct-lookup shortfall, in one clause reusable by the zero-row message and the delivering-run
// status message below (cycle 2352). Before this, a PARTIAL shortfall was invisible everywhere the
// buyer looks: the zero-row branch only fires when NOTHING came back, and `markIncomplete` is
// deliberately not called for not-found/malformed ids (an answered "absent" is a complete answer,
// not a truncated run), so a 10-id lookup that delivered 7 set NO status message at all and read
// in the console exactly like a perfect run. `declaredMatches` is `nctIds.length` -- the POST-drop
// count -- so bad-format ids could not be recovered from the summary arithmetic either.
// The four lists are disjoint by construction in resolveIdsChunk, and `nctIdsBadFormat` never
// entered them, so the counts sum without double-counting.
function lookupShortfallNote() {
    if (!nctIds.length) return '';
    const parts = [];
    let missing = 0;
    const add = (ids, text) => { if (ids.length) { missing += ids.length; parts.push(`${ids.length} ${text}`); } };
    add(notFoundIds, 'not in the registry');
    add(malformedIds, 'rejected by ClinicalTrials.gov as malformed');
    // Kept separate from "not in the registry" for the same reason resolveIdsChunk keeps the lists
    // apart: a request that was never answered cannot support the claim that a study is absent.
    add(failedIds, 'never answered for (NOT known to be missing -- re-run those ids)');
    add(notReachedIds, 'never requested, because the run stopped first');
    add(nctIdsBadFormat, 'dropped before the run as bad format (expected NCT + 8 digits)');
    if (!parts.length) return '';
    const asked = nctIds.length + nctIdsBadFormat.length;
    return ` ${missing} of the ${asked} id(s) you asked for returned no row: ${parts.join('; ')}.`
        + ' See RUN_SUMMARY for the exact id lists.';
}

// Built once and reused below for `setStatusMessage` (cycle 1758) -- until this fix these were
// log-only, so a complete run with 0 rows showed bare "Succeeded" in the Console with the cause
// visible only in the log. Watch-mode SEEDING stays silent (0 rows there is the documented
// by-design baseline result, not an empty search), matching every prior Actor in this audit.
let zeroRowMessage = null;
if (pushed === 0 && watchMode && !seeding) {
    zeroRowMessage = `Nothing new for watch label "${watchLabel}" since its last run -- all ${skippedSeen} matching `
        + 'stud(y/ies) had already been delivered under this label. That is the expected result most of the '
        + 'time; you were charged for nothing.';
    log.warning(zeroRowMessage);
} else if (pushed === 0 && !seeding) {
    if (nctIds.length) {
        // The old wording asserted flatly that every id "was either malformed or not found", which
        // is a claim about the registry that a never-answered request cannot support (and said
        // nothing about ids the run never reached). The note states exactly which outcome each id
        // got instead. (cycle 2352)
        zeroRowMessage = `No studies were returned for the nctId(s) you asked for.${lookupShortfallNote()}`;
        log.warning(zeroRowMessage);
    } else {
        // Log form keeps the full 3-cause explanation (539 chars, past the status-message cap).
        // The status message below is a SEPARATE, compact rendering of the same 3 causes in the
        // same order, written to fit under 500 chars whole rather than relying on
        // clampStatusMessage() to cut it -- a truncated-but-non-null message would still lose
        // cause (3) silently, exactly as it did live before this fix.
        zeroRowMessage = `No studies matched (scanned ${scanned}). Common causes: (1) conditions/interventions/sponsors/`
            + 'locations/searchQuery are ANDed, so several narrow filters together often match nothing -- drop '
            + 'one and retry. (2) phases only applies to interventional studies; pairing it with '
            + 'studyTypes=["OBSERVATIONAL"] always returns nothing. (3) resultsAvailability="with" matches a '
            + 'small minority of studies -- combine with a broader condition first.';
        log.warning(
            `No studies matched. Scanned ${scanned} rows. Most common causes, in order: `
            + '(1) conditions/interventions/sponsors/locations/searchQuery are ANDed — combining several '
            + 'narrow filters often genuinely matches nothing; drop one and retry. '
            + '(2) phases only applies to interventional studies with a phase assigned; pairing it with '
            + 'studyTypes=["OBSERVATIONAL"] always returns nothing. '
            + '(3) resultsAvailability is "with" (or the deprecated hasResultsOnly, which sets the same '
            + 'thing) on a small minority of studies — combine with a broad condition first.',
        );
    }
}

log.info(`Done. Pushed ${pushed} rows over ${pages} page(s) (scanned ${scanned} studies, mode=${rowsPerStudy}).`);

// ---------------------------------------------------------------------------
// RUN_SUMMARY: the completeness of this run, in a form a pipeline can read. Fetch with
//   GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
// which works with no webhook configured. `complete` is deliberately kept OUT of any status
// string: a run is SUCCEEDED and truncated at the same time, and that pair is the exact case this
// record exists for.
const runMode = nctIds.length ? 'direct-lookup' : (watchMode ? (seeding ? 'watch-seed' : 'watch-incremental') : 'search');
const runSummary = {
    mode: runMode,
    // What the registry says matches these filters (search modes) or how many ids were asked for
    // (direct-lookup). `null` means we never got a number -- never assume 0.
    declaredMatches,
    scanned,
    delivered: pushed,
    pages,
    rowsPerStudy,
    complete,
    incompleteReason,
    incompleteDetail,
    maxResults,
    watchLabel: watchMode ? watchLabel : null,
    baselineSize: watchMode ? watchSeen.size : null,
    // Ids the WATCH_KEEP record cap dropped this run / over the life of this label. A dropped id
    // is re-delivered and re-charged later, so this is a billing signal, not just a size stat.
    baselineTruncated: watchMode ? baselineTruncated : null,
    baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
    skippedAlreadyDelivered: watchMode && !seeding ? skippedSeen : null,
    changedRedelivered: watchMode && !seeding ? changedCount : null,
    requestedIds: nctIds.length || null,
    // Ids dropped by our own NCT-format check before any request was made. `requestedIds` (and
    // `declaredMatches`) are the POST-drop count, so without this a pipeline cannot tell that the
    // input asked for more than the run ever looked up. (cycle 2352)
    badFormatIds: nctIds.length ? nctIdsBadFormat : null,
    notFoundIds: nctIds.length ? notFoundIds : null,
    malformedIds: nctIds.length ? malformedIds : null,
    failedIds: nctIds.length ? failedIds : null,
    notReachedIds: nctIds.length ? notReachedIds : null,
    // Machine-readable form of the change-blind-filter warning: a scheduled caller that never
    // reads the log can assert on this being empty before trusting "no changes this run".
    watchChangeBlindFilters: watchMode && watchChanges ? watchChangeBlindFilters : null,
    // Machine-readable form of the dead-date-bound warning. Non-empty means this watch can no
    // longer surface NEW studies at all, however healthy "nothing new" looks -- a scheduled caller
    // should alert on it rather than trust a quiet run.
    watchDeadDateBounds: watchMode ? watchDeadDateBounds : null,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

// A truncated run still SUCCEEDS (the rows we did get are real and already charged), so the status
// message is the only place the Apify console itself shows the shortfall. There was no
// setStatusMessage call anywhere in this Actor before cycle 646.
if (!complete) {
    const of = declaredMatches === null ? '' : ` of ${declaredMatches.toLocaleString('en-US')} declared`;
    // `incompleteReason` is first-cause-wins, so on a direct lookup it names ONE of the things that
    // went wrong (e.g. 'max-results') and stays silent about the rest; the shortfall note
    // enumerates them all. truncationNote() and the note can never both be non-empty -- that one
    // is watch-mode only, and watchMode requires `nctIds.length === 0`.
    await Actor.setStatusMessage(clampStatusMessage(
        `Incomplete: ${pushed.toLocaleString('en-US')} row(s)${of} — ${incompleteReason}`
        + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. See RUN_SUMMARY for details.`
        + truncationNote() + lookupShortfallNote(),
    ));
} else if (baselineTruncated > 0) {
    // A complete run that evicted baseline ids would otherwise show nothing in the console at all
    // -- the shortfall is in a future bill, not in this run's row count.
    await Actor.setStatusMessage(
        (seeding
            ? `Baseline run for watch label "${watchLabel}": ${watchSeen.size.toLocaleString('en-US')} stud(y/ies) recorded, 0 charged.`
            : `Watch label "${watchLabel}": ${pushed.toLocaleString('en-US')} row(s) delivered.`)
        + truncationNote(),
    );
} else if (zeroRowMessage) {
    // clampStatusMessage() is a backstop only -- the compact plain-no-match wording above is
    // already written to fit whole; this guards the watch-label branch, whose length depends on
    // a user-supplied watchLabel string with no schema-enforced length cap.
    await Actor.setStatusMessage(clampStatusMessage(zeroRowMessage));
} else if (nctIds.length && lookupShortfallNote()) {
    // A DELIVERING direct lookup that still came up short on some ids. Reached only when the run is
    // otherwise complete (`!complete` is handled above), i.e. the shortfall is not-found/malformed/
    // bad-format ids -- real answers, but not the ones the buyer's row count implies. This arm is
    // the whole point of the cycle-2352 fix: without it these runs set no status message at all.
    await Actor.setStatusMessage(clampStatusMessage(
        `Delivered ${pushed.toLocaleString('en-US')} row(s).${lookupShortfallNote()}`,
    ));
} else if (declaredMatches !== null && !watchMode && !nctIds.length) {
    log.info(`Complete: delivered every one of the ${declaredMatches.toLocaleString('en-US')} studies the registry declared for these filters.`);
}

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill -- best-effort only, one attempt, short timeout, failures are
// a warning not a thrown error.
if (webhookUrl) {
    const env = Actor.getEnv();
    const payload = {
        actorRunId: env.actorRunId ?? null,
        defaultDatasetId: env.defaultDatasetId ?? null,
        finishedAt: new Date().toISOString(),
        pushed,
        scanned,
        pages,
        watchLabel: watchMode ? watchLabel : null,
        watchSeeding: watchMode ? seeding : null,
        watchNewCount: watchMode && !seeding ? pushed - changedCount : null,
        watchChangedCount: watchMode && !seeding ? changedCount : null,
        // Same object as the RUN_SUMMARY key-value record, for subscribers who would rather not
        // make a second call to find out whether the result set was complete.
        summary: runSummary,
    };
    try {
        const resp = await gotScraping({
            url: webhookUrl,
            method: 'POST',
            responseType: 'text',
            throwHttpErrors: false,
            retry: { limit: 0 },
            timeout: { request: 10000 },
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (resp.statusCode >= 400) log.warning(`webhookUrl POST returned ${resp.statusCode}; run result is unaffected.`);
        else log.info(`Posted completion summary to webhookUrl (${resp.statusCode}).`);
    } catch (err) {
        log.warning(`webhookUrl POST failed (${err.message}); run result is unaffected.`);
    }
}

// Deferred to the very last statement on purpose (h289): failing any earlier would skip the
// RUN_SUMMARY write and the webhook above. A seed pushes no rows, so nothing was charged and
// failing is free -- and failing loudly, instead of exiting 0 with no baseline saved, stops a
// scheduled run from quietly reading "seeded" and moving on to incremental.
if (watchMode && seedFailure) {
    await Actor.fail(
        `The watch baseline could not be completed: ${seedFailure.replace(/[.\s]*$/, '')}. No baseline was saved `
        + '(a partial one would cause you to be charged twice for the same studies later) and nothing was '
        + `charged. ${seedFailureIsInputError
            ? 'This is ClinicalTrials.gov rejecting your input (an unrecognised filter value) -- re-running with '
                + 'the same input will fail the same way; fix the filter values above and re-run.'
            : seedFailureIsTimeBudget
                ? 'The run hit its own time limit with ClinicalTrials.gov still answering -- re-running unchanged '
                    + 'will stop at the same place; raise the run timeout or narrow the query, then re-run.'
                : 'Please re-run in a few minutes.'}`,
    );
}

await Actor.exit();
