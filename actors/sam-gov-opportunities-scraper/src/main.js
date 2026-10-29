import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
// Soft-deadline guard (same pattern as google-news-scraper:11-20, 21st Actor on the rollout).
// This Actor can approach the platform run timeout with real work still queued in two places: the
// paged search walk (up to 100 pages x 300ms pacing, plus up to 4 retries x 2-12s per failed page)
// and the per-row enrich/attachments pass (1-2 HTTP calls + 200-400ms sleep for EVERY delivered
// row). Getting hard-killed there is not a billing loss -- pushResult charges per row as it goes --
// it is the skipped writes AFTER the walk: RUN_SUMMARY and, worse, the watch-state
// `watchStore.setValue`, so a watch-mode buyer whose run is killed loses their baseline and gets
// re-charged for the whole result set next run. Stop proactively with a margin and flush instead.
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
let timeBudgetExceeded = false;
// Milliseconds of useful work left before the margin starts. Infinity on a local/dev run, where
// the platform sets no deadline.
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
function timeBudgetOk() {
    if (remainingMs() <= 0) { timeBudgetExceeded = true; return false; }
    return true;
}
const input = (await Actor.getInput()) ?? {};

// SAM.gov's OFFICIAL developer API (api.sam.gov/opportunities/v2/search) requires a free
// registered API key (confirmed against open.gsa.gov's own docs, cycle 538). This Actor instead
// uses the same undocumented, unauthenticated backend that powers sam.gov's own public search
// PAGE -- verified live cycle 538/539 with 5+ spaced requests (all 200, ~0.2s, no block/challenge)
// and real pagination/filters. Same class of finding as trademark-search-scraper's TMview
// endpoint (cycle 512): a public government site's own search-UI backend, not its registered
// developer API, no ToS click-through, no login, no key.
const SEARCH_API = 'https://sam.gov/api/prod/sgs/v1/search/';
const DETAIL_API = 'https://sam.gov/api/prod/opps/v2/opportunities';
// Same keyless backend, a v3 endpoint distinct from DETAIL_API's v2 -- the detail call's own
// `additionalInfo.sections` lists an "attachments-links" section but never the files themselves.
// Probed live cycle 1133: `GET .../opps/v3/opportunities/<id>/resources` returns the real list, and
// `.../opps/v3/opportunities/resources/files/<resourceId>/download` 303-redirects to a presigned,
// public (no key/login/cookie) S3 URL -- but that redirect target expires in ~9 seconds, so the
// STABLE sam.gov URL is what gets published, not the presigned one, which would be dead before a
// buyer's pipeline got to it.
const ATTACHMENTS_API = 'https://sam.gov/api/prod/opps/v3/opportunities';
function attachmentDownloadUrl(resourceId) {
    return `${ATTACHMENTS_API}/resources/files/${resourceId}/download`;
}

// The SAME keyless backend multiplexes several of SAM.gov's public data types behind `index=`
// (cycle 703's rule, cycle 704's build). Probed live cycle 704/707, all 200 OK with no key/login:
//   index=opp  -> contract opportunities (what this Actor shipped with)
//   index=dbra -> Davis-Bacon Act construction wage determinations (`_type: wdDBRA`, 85,426)
//   index=wd   -> Collective Bargaining Agreement wage determinations (`_type: wdCBA`, 107,580)
//   index=sca  -> Service Contract Act wage determinations (`_type: wdSCA`, 2,666)
//   index=cfda -> CFDA assistance listings -- grants/loans/direct-payment programs
//                 (`_type: assistanceListing`, 7,392, ~2,871 active)
//   index=ei   -> exclusions (federal debarment/suspension list, `_type: exclusion`, 168,673 total
//                 -- but see the MANDATORY classification filter below; this Actor never serves the
//                 79% of that index that names private individuals)
// `index=dbra` was NOT in cycle 703's scoping (it guessed `dba`/`wdol`/`davisbacon`, all 400) --
// `wd` alone is CBA-only, so shipping just `wd` would have silently omitted the Davis-Bacon set,
// which is the one construction contractors actually need. One index per run on purpose: the
// completeness machinery below measures ONE `page.totalElements` per run, and merging two indices
// would make `declaredMatches` unreadable.
const DATA_TYPES = {
    'opportunities': { index: 'opp', noun: 'opportunity', nounPlural: 'opportunities' },
    'wage-determinations-dbra': { index: 'dbra', noun: 'wage determination', nounPlural: 'wage determinations' },
    'wage-determinations-cba': { index: 'wd', noun: 'wage determination', nounPlural: 'wage determinations' },
    'wage-determinations-sca': { index: 'sca', noun: 'wage determination', nounPlural: 'wage determinations' },
    'assistance-listings': { index: 'cfda', noun: 'assistance listing', nounPlural: 'assistance listings' },
    'exclusions': { index: 'ei', noun: 'exclusion record', nounPlural: 'exclusion records' },
};
// A 4th distinct row family (opp / wd / cfda / ei) needs its own dispatch, not a 2-way `isWd`
// boolean (cycle 706's note) -- one map from dataType to family, `isWd`/`isCfda`/`isExclusions`
// derived from it below.
const DATA_TYPE_FAMILY = {
    'opportunities': 'opp',
    'wage-determinations-dbra': 'wd',
    'wage-determinations-cba': 'wd',
    'wage-determinations-sca': 'wd',
    'assistance-listings': 'cfda',
    'exclusions': 'ei',
};

// Confirmed live cycle 539: `notice_type` takes SAM's own single-letter codes (matches the
// codes SAM shows in the UI dropdown / that come back on each row's `type.code`).
// Cycle 835 facet-diff: single-letter probe a-z/0-9 against `notice_type=<c>` found 4 more real,
// non-empty codes SAM's current UI dropdown never lists -- all 4 are legacy/retired (most recent
// `modifiedDate` across all of them is 2020-03-31; none has posted since), predating the ~2019
// notice-type consolidation, but the underlying historical rows are real and otherwise
// unfilterable: m=1,058, f=187, j=86,674, l=9,520 (97,439 rows total). Kept separate from the 9
// live codes above so the schema/README can flag them as historical-only.
const NOTICE_TYPE_CODES = {
    p: 'Presolicitation', o: 'Solicitation', k: 'Combined Synopsis/Solicitation',
    r: 'Sources Sought', a: 'Award Notice', s: 'Special Notice', g: 'Sale of Surplus',
    i: 'Intent to Bundle', u: 'Justification',
    m: 'Modification/Amendment/Cancel (legacy, retired ~2020)',
    f: 'Foreign Government Standard (legacy, retired ~2019)',
    j: 'Justification and Approval (J&A) (legacy, retired ~2019)',
    l: 'Fair Opportunity/Limited Sources Justification (legacy, retired ~2019)',
};

// SAM.gov's `set_aside` values are CASE-SENSITIVE, and `setAsideTypes` is a free-text stringList
// with no schema enum -- so unlike `noticeTypes` (enum, platform-validated before the run starts)
// nothing stops a buyer from sending a spelling this backend does not recognise. A bad VALUE fails
// CLOSED here (0 rows, HTTP 200, no error -- cycle 708/748), which is billing-safe but
// indistinguishable from "there genuinely are no matching opportunities". Measured live cycle 1008:
//   SBA 1,204,971 | 8A 20,742 | SDVOSBC 156,143 | BICiv 4,498      (real codes)
//   sba 0 | 8a 0 | 8(a) 0 | SDVOSB 0 | "small business" 0          (buyer-natural spellings)
// So `setAsideTypes: ["sba"]` -- lowercase, the single most likely typo -- silently returned zero
// rows on the largest set-aside category in the index.
//
// The naive fix (`.toUpperCase()`, copying how `states` is normalised 120 lines below) is WRONG and
// would have introduced a worse bug than it fixed: `BICiv` (Buy Indian Set-Aside) is genuinely
// mixed-case upstream -- measured live cycle 1008, `BICiv` -> 4,498 rows but `BICIV` -> 0. Blanket
// uppercasing would have broken the one code that was previously working for anyone who copied it
// correctly. Hence a canonical map keyed by lowercase, emitting the platform's exact spelling.
//
// Every code below was verified non-zero live against index=opp in cycle 1008, and re-verified
// non-zero (0 dead values, counts within natural growth) in cycle 1524. SAM.gov publishes no
// facet/reference endpoint for this vocabulary (re-checked cycle 1524: still no `facets`/
// `aggregations` in the search response at any param spelling; `locationservices/v1/api/
// setasidetypes` still 500s; opps/v1|v2/setasides and referencedata/v1/setAsideTypes all 404), so
// this list is maintained by live probe, not sync.
const SET_ASIDE_CODES = [
    'SBA', 'SBP', '8A', '8AN', 'HZC', 'HZS', 'SDVOSBC', 'SDVOSBS',
    'WOSB', 'WOSBSS', 'EDWOSB', 'EDWOSBSS', 'LAS', 'IEE', 'ISBEE', 'BICiv', 'VSA', 'VSS',
];
// Cycle 1524 ran the OTHER direction of this audit for the first time (upstream - ours, not just
// ours - upstream: every prior pass only re-verified that OUR 18 codes still return rows). With no
// facet endpoint to read the vocabulary from, it was derived empirically two ways: (a) 1,500 live
// search rows sampled across the index, reading each row's own `solicitation.setAside.code`, and
// (b) a brute-force probe of the whole 1- and 2-character alphanumeric code space (1,332 values --
// only `8A` is real, so that space is now closed and any further unknown code must be 3+ chars).
// That surfaced 3 real, filterable codes this list never had. Two are retired programs with zero
// active rows -- same class as the legacy m/f/j/l notice types above, real historical rows that no
// other filter can reach: SDB "Total Small Disadvantage Business" (464 rows, newest modified
// 2019-06-27) and ESB "Emerging Small Business" (714 rows, newest 2020-01-20). The third, NONE, is
// very much alive (38,997 rows, 3,349 of them active, newest modified the day of the audit) and is
// SAM.gov's explicit "no set-aside / unrestricted" marker -- it is NOT a synonym for leaving this
// filter empty, because the ~4.2M unrestricted rows that carry no setAside object at all are not
// in it. Before this, all three were treated as typos: still sent (fail-closed by design) and so
// still working, but the run warned they would match ZERO rows, which was simply false.
const SET_ASIDE_CODES_HISTORICAL = ['SDB', 'ESB'];
const SET_ASIDE_CODE_UNRESTRICTED = 'NONE';
const SET_ASIDE_CODES_ACCEPTED = [...SET_ASIDE_CODES, SET_ASIDE_CODE_UNRESTRICTED, ...SET_ASIDE_CODES_HISTORICAL];
const SET_ASIDE_BY_LOWER = new Map(SET_ASIDE_CODES_ACCEPTED.map((c) => [c.toLowerCase(), c]));
// Aliases for the umbrella names the README's own use-cases advertise ("8(a) / SDVOSB capture"),
// which are NOT codes this backend accepts. Each expands to the real code(s) it covers -- SAM.gov
// splits SDVOSB and HUBZone into separate competitive/sole-source codes, and a buyer asking for
// "SDVOSB" means either, so the alias expands to both rather than silently picking one. The filter
// is an OR-union already (comma-joined), so expanding is exactly the intended semantics.
const SET_ASIDE_ALIASES = {
    '8(a)': ['8A'],
    'sdvosb': ['SDVOSBC', 'SDVOSBS'],
    'hubzone': ['HZC', 'HZS'],
};

// Maps a buyer's `setAsideTypes` to the spellings SAM.gov accepts. Unrecognised values are KEPT, not
// dropped: dropping them could empty the list and make the whole filter vanish from the query, which
// fails OPEN (the unfiltered index, every row pushed and CHARGED -- the cycle 748 failure mode).
// Keeping an unknown value preserves the safe fail-closed 0-row outcome; the warning is what makes
// it visible. This is the opposite call from grants-gov-scraper's agency-code drop (cycle 1002),
// because there dropping the filter was the documented, harmless fallback and here it is the hazard.
function canonSetAsides(values) {
    const out = [];
    const unknown = [];
    const expanded = [];
    for (const v of values) {
        const lower = v.toLowerCase();
        if (Object.hasOwn(SET_ASIDE_ALIASES, lower)) {
            const codes = SET_ASIDE_ALIASES[lower];
            expanded.push(`${v} -> ${codes.join(',')}`);
            out.push(...codes);
        } else if (SET_ASIDE_BY_LOWER.has(lower)) {
            const canon = SET_ASIDE_BY_LOWER.get(lower);
            if (canon !== v) expanded.push(`${v} -> ${canon}`);
            out.push(canon);
        } else {
            unknown.push(v);
            out.push(v);
        }
    }
    if (expanded.length) {
        log.info(`setAsideTypes normalised to SAM.gov's case-sensitive codes: ${expanded.join('; ')}.`);
    }
    // NONE is the one accepted value whose plain-English reading ("no set-aside filter") is the
    // opposite of what it does upstream, so say so rather than letting it look like a no-op.
    if (out.includes(SET_ASIDE_CODE_UNRESTRICTED)) {
        log.info(
            'setAsideTypes includes NONE, SAM.gov\'s explicit "unrestricted / no set-aside" marker. This NARROWS '
            + 'the search to the ~39k opportunities SAM.gov tagged NONE outright -- it is not the same as leaving '
            + 'setAsideTypes empty, which searches every opportunity including the millions that carry no '
            + 'set-aside field at all.',
        );
    }
    const historical = out.filter((c) => SET_ASIDE_CODES_HISTORICAL.includes(c));
    if (historical.length) {
        log.info(
            `setAsideTypes includes retired set-aside program(s) ${historical.join(', ')}. These match real `
            + 'historical opportunities (SDB ~464, ESB ~714) but ZERO active ones -- nothing has posted under '
            + 'either since 2020. Useful for research, not for a current-bid pipeline.',
        );
    }
    if (unknown.length) {
        log.warning(
            `setAsideTypes value(s) ${unknown.map((v) => `"${v}"`).join(', ')} are not SAM.gov set-aside codes. `
            + 'They are still sent, and SAM.gov fails closed on an unrecognised value, so they will match ZERO '
            + 'opportunities rather than widening your results. If you expected matches, use one of: '
            + `${SET_ASIDE_CODES.join(', ')} (or the aliases 8(a), SDVOSB, HUBZone; or NONE for explicitly `
            + `unrestricted, or the retired ${SET_ASIDE_CODES_HISTORICAL.join('/')} for historical rows only).`,
        );
    }
    return [...new Set(out)];
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---------------------------------------------------------------------------
// Run-level completeness (cycle 649, h250 class). Before this, EVERY way this Actor could come up
// short was invisible to a pipeline: a page that 500s mid-walk just `break`s out of fetchRows(),
// SAM's 10,000-row backend depth cap only produced an English log line, maxResults and the PPE
// charge limit stopped the push loop silently, and `totalElements` -- the only number that says how
// many opportunities actually matched -- was never written anywhere the buyer can read. 200 rows of
// a 12,297-match query looked exactly like exhausting a 200-match query. Same contract as
// nih-reporter-scraper / fda-recall-scraper / clinicaltrials-scraper: a RUN_SUMMARY key-value
// record, a status message, and the same object on the webhook payload.
let declaredMatches = null;   // SAM's own page.totalElements for this query; null = never answered, NEVER 0
let scanned = 0;              // raw search rows read back from the API
let pages = 0;
let pagesFailed = 0;
let duplicateRowsDropped = 0; // rows SAM.gov served more than once; dropped before any charge
// SAM.gov sometimes posts the SAME solicitation twice under two brand-new opportunityIds, seconds
// apart (measured live 2026-09-24, 400-row activeOnly opportunities sample: 2.2%, up to 3 copies of
// one VA notice at 14:11:11/:12/:12) -- id-keyed `seenIds` above can never catch this, since the id
// itself is what differs. Same defect class as `uk-find-a-tender-scraper` cycle 760's republication
// finding: content-level redundancy is a different defect from filter fidelity, and only a
// same-source content hash (never cross-record-shape) catches it without over-merging genuinely
// distinct opportunities that happen to share a title. Opportunities-shape only (isWd/isCfda/
// isExclusions rows were not part of this measurement and are not covered).
let republishedRowsDropped = 0;
// SAM.gov's own do-not-display marker on the exclusions index -- every sampled row carries "F",
// but any row marked "T" must be dropped regardless of classification (cycle 708 finding). Counted
// separately from duplicates so RUN_SUMMARY doesn't conflate "SAM repeated a row" with "SAM said
// don't show this one".
let noPublicDisplaySuppressed = 0;
let complete = true;
let incompleteReason = null;
let incompleteDetail = null;
let lastApiError = null;      // WHY the most recent null happened, carried into RUN_SUMMARY

// First cause wins: a walk that stopped because SAM stopped answering and THEN also hit maxResults
// must keep reporting the upstream failure -- that is the cause the buyer can act on.
// ...with ONE exception, found live while testing the time-budget guard: `max-results` is marked
// BEFORE the push loop runs (the walk got everything it was asked for, SAM just has more behind
// it), it is the buyer's own chosen ceiling, and it is already the weakest cause in this file --
// charge-limit outranks it below for exactly that reason. A time-budget stop inside the push loop
// is strictly more actionable AND falsifies the earlier mark, because fewer rows than maxResults
// were actually delivered. Without this exception a clock-stopped run on any query larger than
// maxResults reported "max-results" and the time budget was invisible in both the status message
// and RUN_SUMMARY -- verified live before the fix (10 of 25 rows delivered, reason "max-results").
function markIncomplete(reason, detail = null) {
    if (!complete && !(reason === 'time-budget' && incompleteReason === 'max-results')) return;
    complete = false;
    incompleteReason = reason;
    incompleteDetail = detail;
}

// One wording for every `time-budget` stop, so the search walk, the seed walk and the per-row
// enrichment pass cannot drift apart. Deliberately says what to CHANGE: "re-run and hope" is the
// right advice for an upstream failure and the wrong advice here -- re-running the same oversized
// query under the same timeout stops in exactly the same place.
function timeBudgetDetail(rowCount) {
    const reach = reachable();
    return `the run approached its platform time limit after ${rowCount.toLocaleString('en-US')} row(s)`
        + `${reach === null ? '' : ` of ${reach.toLocaleString('en-US')} reachable`} over ${pages} page(s), `
        + 'and stopped itself so the rows already collected (and, in watch mode, the baseline) would be saved '
        + 'instead of lost to a hard kill. Narrow the query or raise maxResults less, or give the run a longer '
        + 'timeout in its run options.';
}

async function apiGet(url) {
    for (let attempt = 1; attempt <= 4; attempt += 1) {
        // Checked per ATTEMPT, not once per call: a retry is only worth starting if there is time
        // left to use its answer, and the backoff sleeps below are capped at the time actually
        // remaining so one long backoff can never sleep straight past the run deadline. The caller
        // distinguishes this null from a real upstream failure via `timeBudgetExceeded`.
        if (!timeBudgetOk()) {
            lastApiError = 'stopped before the run time budget ran out';
            log.warning('Run time budget reached; not starting another SAM.gov request.');
            return null;
        }
        let resp;
        try {
            resp = await gotScraping({
                url,
                method: 'GET',
                responseType: 'text',
                throwHttpErrors: false,
                retry: { limit: 0 },
                timeout: { request: 30000 },
                headers: { accept: 'application/hal+json' }, // required: plain application/json 406s (cycle 539)
            });
        } catch (err) {
            lastApiError = `request error: ${err.message}`;
            log.warning(`SAM.gov request failed (${err.message}); retrying (${attempt}/4).`);
            await sleep(Math.max(Math.min(attempt * 2000, remainingMs()), 0));
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            lastApiError = `HTTP ${resp.statusCode}`;
            log.warning(`SAM.gov returned ${resp.statusCode}; retrying (${attempt}/4).`);
            await sleep(Math.max(Math.min(attempt * 3000, remainingMs()), 0));
            continue;
        }
        if (resp.statusCode === 404) { lastApiError = 'HTTP 404'; return null; }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200 || !parsed) {
            lastApiError = `HTTP ${resp.statusCode}, non-JSON or unexpected body`;
            log.warning(`SAM.gov ${url} returned ${resp.statusCode}, non-JSON or unexpected body: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        return parsed;
    }
    lastApiError = lastApiError ?? 'exhausted 4 attempts';
    log.warning(`SAM.gov ${url} kept failing after 4 attempts; skipping.`);
    return null;
}

const dataTypeRaw = String(input.dataType ?? 'opportunities').trim();
const dataType = Object.hasOwn(DATA_TYPES, dataTypeRaw) ? dataTypeRaw : 'opportunities';
if (dataType !== dataTypeRaw) {
    log.warning(`dataType "${dataTypeRaw}" is not one of ${Object.keys(DATA_TYPES).join(', ')}; falling back to "opportunities".`);
}
const { index: SEARCH_INDEX, noun: ROW_NOUN, nounPlural: ROW_NOUN_PLURAL } = DATA_TYPES[dataType];
const recordFamily = DATA_TYPE_FAMILY[dataType];
const isWd = recordFamily === 'wd';
const isCfda = recordFamily === 'cfda';
const isExclusions = recordFamily === 'ei';

// Cycle 96 seed rule: never ship a default that makes the very first test run return 0 rows.
// On the wage-determination indices a keyword is the WRONG default: `q` there matches the
// determination's reference number, not the trades inside it (measured cycle 704: `q=roofing`
// returns 0 against 85,426 live Davis-Bacon rows), so defaulting to "contract" would hand a first
// run an empty dataset. Seed those modes with no keyword instead -- an unfiltered wd query is
// itself a valid, large result set. `q=contract` on the cfda index is technically non-zero
// (176/7,392, measured cycle 707) but is a construction/procurement term that has nothing to do
// with grant programs and would bias a first-run sample toward an unrepresentative slice --
// same "no keyword" treatment as wd, for a different reason (irrelevance, not a zero-match trap).
// Exclusions gets the same empty-keyword default: `q=construction` on `index=ei` is non-zero
// (253/35,195, measured cycle 708/709) but entity names have nothing to do with construction, so
// defaulting to it would bias a first run toward an unrepresentative slice, same reasoning as cfda.
const keyword = String(input.keyword ?? (isWd || isCfda || isExclusions ? '' : 'contract')).trim();
// THE BLANK-ENTRY DROP (cycle 2356). Every array filter here normalises with
// `.map(trim).filter(Boolean)`, so an empty or whitespace-only entry is DROPPED -- and if every
// entry the buyer sent was blank, the list ends up empty and `buildSearchUrl` below then OMITS the
// filter param entirely. That is not a zero-row result, it is an UNFILTERED one, pushed and CHARGED
// in full. Measured live cycle 2356 on index=opp under this Actor's own default
// `q=contract&is_active=true`: dropping `naics=541511` widens 33 -> 16,110 matches (488x), dropping
// `pop_state=TX` widens 194 -> 16,110 (83x), dropping `set_aside=SBA` widens 3,405 -> 16,110 (4.7x).
// Nothing else in this file can see it. The cycle-748 canary (`assertFilterNamesApplied`) only
// probes filter NAMES the run is actually about to use, and an emptied list is not one. The
// unknown-set-aside warning at `canonSetAsides` cannot fire, because the blank never reaches it --
// which is the gap in that function's own cycle-748 reasoning ("dropping them could empty the list
// and make the whole filter vanish from the query, which fails OPEN"): it holds the line for
// unrecognised values and the `.filter(Boolean)` one call upstream of it breaks the same line for
// blank ones. And the zero-row `appliedFilters` list is only reached when 0 rows come back, which
// is precisely what a widened query does not do.
// Blank entries are reachable, not theoretical: verified live cycle 2356 that the Apify platform
// ACCEPTS `naicsCodes: [""]`, `states: [""]` and `setAsideTypes: [""]` on an API-started run (three
// real runs, all created then aborted). That is exactly the shape an input built from a spreadsheet
// column with an empty cell, or a templated schedule input, produces. `noticeTypes` is the one
// array input the platform guards for us, because it is the only one with an `items.enum` -- also
// verified live the same cycle: `noticeTypes: ["zzz"]` is rejected with HTTP 400 `invalid-input`
// BEFORE the run starts, so its `Object.hasOwn(NOTICE_TYPE_CODES, ...)` filter below can only ever
// drop a blank, never an unrecognised code. Do not rely on that for a stringList field: a schema
// `enum` is enforced, a free-text `stringList` is not.
const blankFilterEntriesDropped = {};
async function arrayFilterInput(name, normalise) {
    const raw = Array.isArray(input[name]) ? input[name] : [];
    const kept = raw.map((v) => String(v).trim()).filter(Boolean);
    if (raw.length > kept.length) blankFilterEntriesDropped[name] = raw.length - kept.length;
    if (raw.length && !kept.length) {
        // Pre-charge, pre-request: an input mistake the buyer can fix, not an upstream failure.
        // Actor.fail() (not a bare throw) so the Console's statusMessage actually carries this
        // reason -- a bare throw lands only in the run log as a stack trace (verified empty
        // statusMessage on run FfhUjzXTncYh3iQvh, cycle 2357 follow-up to cycle 2356's fix).
        await Actor.fail(
            `Every one of the ${raw.length} value(s) you gave in \`${name}\` is empty or whitespace-only, so the `
            + `filter would have been dropped from the SAM.gov query entirely and this run would have searched `
            + `UNFILTERED by ${name} -- not zero rows, but the whole unnarrowed result set, every row of it pushed `
            + `and charged (measured: an opportunities search narrowed by one NAICS code returns ~33 matches, the `
            + `same search with the naics filter missing returns ~16,110). Stopping before any unfiltered row is `
            + `delivered or charged. Put real values in \`${name}\`, or remove the field to search without it `
            + `deliberately.`,
        );
    }
    return normalise ? normalise(kept) : kept;
}
const naicsCodes = await arrayFilterInput('naicsCodes');
const setAsideTypes = await arrayFilterInput('setAsideTypes', canonSetAsides);
const noticeTypes = await arrayFilterInput(
    'noticeTypes',
    (kept) => kept.map((v) => v.toLowerCase()).filter((v) => Object.hasOwn(NOTICE_TYPE_CODES, v)),
);
const states = await arrayFilterInput('states', (kept) => kept.map((v) => v.toUpperCase()));
// A PARTIAL blank drop still applies the surviving values, so it is a warning rather than a stop --
// but it is a silent narrowing of what the buyer asked for, so it also has to reach a surface the
// Console shows (see `blankDropNote()`, appended to every status message below) and RUN_SUMMARY.
// Without that, the only trace of it is this one console line.
if (Object.keys(blankFilterEntriesDropped).length) {
    log.warning(
        `Ignored blank/whitespace-only entries in ${Object.entries(blankFilterEntriesDropped)
            .map(([f, n]) => `${f} (${n})`).join(', ')}. The non-blank values you gave are still applied; `
        + 'a blank is never sent to SAM.gov, because an unrecognised value there matches nothing.',
    );
}
function blankDropNote() {
    const fields = Object.entries(blankFilterEntriesDropped);
    if (!fields.length) return '';
    return ` NOTE: ${fields.map(([f, n]) => `${n} blank entr${n === 1 ? 'y' : 'ies'} in ${f}`).join(', ')} `
        + 'ignored (not guessed at); the non-blank values you gave still applied.';
}
const organizationId = String(input.organizationId ?? '').trim();
const activeOnly = input.activeOnly !== false; // default true

// POSTED / DEADLINE DATE WINDOWS (cycle 2392). SAM.gov's search backend exposes no date-range
// parameter on ANY of these indices -- re-probed across several cycles, and this Actor's own FAQ
// has said so since cycle 540 -- so unlike every other filter here these four are POST-FETCH:
// the row is read, normalised, then dropped BEFORE pushResult(), so it is never pushed and never
// charged. Three consequences a buyer has to be told about, all documented in the input schema:
// the window does NOT reduce how much is read upstream (the walk keeps paging until `maxResults`
// in-window rows are found, so a narrow window over a broad keyword can exhaust the time budget),
// `declaredMatches` in RUN_SUMMARY stays SAM.gov's own PRE-window count, and a run can therefore
// deliver far fewer rows than SAM declared without being incomplete (see the empty-page
// reconciliation in fetchRows, which had to learn about this or every windowed run would end on a
// false `short-page`).
//
// Both ends are INCLUSIVE and compared on the CALENDAR DATE THE ROW ITSELF CARRIES -- the leading
// `YYYY-MM-DD` of its timestamp, never re-zoned. SAM.gov emits three shapes on these fields
// (`2026-10-15T04:00:00.000Z` on wd rows normalised from epoch ms, `2026-01-16T00:02:55-05:00`,
// `2023-07-12T19:23:54+00:00`); converting to UTC first would shift an evening US-Eastern posting
// onto the next day and silently drop rows from a window the buyer thinks they asked for, while
// the date as published is what sam.gov's own notice page shows.
const CAL_DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
async function dateWindowInput(name) {
    const raw = String(input[name] ?? '').trim();
    if (!raw) return null;
    // A date window that cannot be parsed must never be silently dropped. A bad keyword fails
    // CLOSED (zero rows, zero charge); a dropped date window fails OPEN -- every row outside the
    // window is delivered AND CHARGED, which is the cycle-748 failure mode this file stops for
    // everywhere else. So: same Actor.fail() treatment as the all-blank stringList above, pre-
    // request and pre-charge. Actor.fail() (not a bare throw) so the reason reaches the Console's
    // statusMessage, per the cycle-2357 finding.
    const asUtc = CAL_DATE_RE.test(raw) ? new Date(`${raw}T00:00:00Z`) : null;
    // The round-trip comparison is what rejects a well-shaped but non-existent date: JS rolls
    // `2026-02-31` forward to 2026-03-03 instead of failing, so matching the regex is not enough.
    if (!asUtc || Number.isNaN(asUtc.getTime()) || asUtc.toISOString().slice(0, 10) !== raw) {
        await Actor.fail(
            `\`${name}\` must be a real calendar date in YYYY-MM-DD form (e.g. 2026-01-31); got "${raw}". `
            + 'Stopping before any row is delivered or charged: an unreadable date window cannot be applied, and '
            + 'ignoring it would hand you the whole unwindowed result set -- every row of it billed -- while '
            + 'looking like it had been filtered. Fix the value, or remove the field to search without a date '
            + 'window deliberately.',
        );
    }
    return raw;
}
const postedFrom = await dateWindowInput('postedFrom');
const postedTo = await dateWindowInput('postedTo');
const deadlineFrom = await dateWindowInput('deadlineFrom');
const deadlineTo = await dateWindowInput('deadlineTo');
// An inverted window is empty by construction: the run could only ever return 0 rows, and the
// zero-row status message would blame "SAM.gov has none once your filters are applied" for what is
// purely an input transposition. Cheaper and clearer to say so before the first request.
// String comparison is sound here -- both sides are validated, zero-padded YYYY-MM-DD.
for (const [fromName, fromVal, toName, toVal] of [
    ['postedFrom', postedFrom, 'postedTo', postedTo],
    ['deadlineFrom', deadlineFrom, 'deadlineTo', deadlineTo],
]) {
    if (fromVal && toVal && fromVal > toVal) {
        await Actor.fail(
            `\`${fromName}\` (${fromVal}) is AFTER \`${toName}\` (${toVal}), so the window is empty and this run `
            + 'could only ever return 0 rows no matter what SAM.gov holds. Swap the two values (the "From" field is '
            + 'the earlier date). Stopping before any request so you are charged nothing.',
        );
    }
}
// Which index carries which date, read off the normalisers in this file rather than assumed:
// `publishDate` is emitted by normalizeRow, normalizeWdRow and normalizeCfdaRow, but the
// exclusions row shape has no publish date at all (it carries activationDate/terminationDate
// instead); `responseDate` is a solicitation response deadline and exists on opportunities only.
// Unlike naicsCodes/setAsideTypes/states, which are WARNED-AND-IGNORED on the dataTypes that do
// not support them, an unsupported date window STOPS the run. The deviation is deliberate: those
// are server-side filters whose warn-and-ignore behaviour predates paying buyers and cannot be
// changed without breaking existing runs, whereas these four fields are brand new (nothing
// depends on them yet) and ignoring one would bill the buyer for the entire unwindowed set.
// Fail closed while it is still free to do so.
const postedWindowSupported = !isExclusions;
const deadlineWindowSupported = !isWd && !isCfda && !isExclusions;
const unsupportedWindowFields = [];
if (!postedWindowSupported) {
    if (postedFrom) unsupportedWindowFields.push('postedFrom');
    if (postedTo) unsupportedWindowFields.push('postedTo');
}
if (!deadlineWindowSupported) {
    if (deadlineFrom) unsupportedWindowFields.push('deadlineFrom');
    if (deadlineTo) unsupportedWindowFields.push('deadlineTo');
}
if (unsupportedWindowFields.length) {
    const why = unsupportedWindowFields.every((f) => f.startsWith('deadline'))
        ? `a response/bid deadline is a property of a contract opportunity -- SAM.gov's "${dataType}" records have no `
          + 'such field, so there is nothing to compare your window against'
        : `SAM.gov's exclusion records carry no publish date at all (they carry \`activationDate\`/`
          + '`terminationDate` instead), so there is nothing to compare your window against';
    await Actor.fail(
        `${unsupportedWindowFields.join(', ')} ${unsupportedWindowFields.length === 1 ? 'is' : 'are'} not supported `
        + `for dataType "${dataType}": ${why}. Stopping before any row is delivered or charged -- ignoring the `
        + 'window would hand you every record matching your other filters, billed in full, while looking filtered. '
        + (unsupportedWindowFields.every((f) => f.startsWith('deadline'))
            ? 'Use dataType "opportunities" for deadline windows'
            + (postedWindowSupported ? ', or filter this dataType by `postedFrom`/`postedTo` instead' : '')
            : 'Filter exclusions by `keyword`/`organizationId` and compare each row\'s own '
              + '`activationDate`/`terminationDate` after delivery')
        + '.',
    );
}
const dateWindowActive = Boolean(postedFrom || postedTo || deadlineFrom || deadlineTo);
let dateWindowDropped = 0; // rows read but outside the requested window -- never pushed, never charged
let dateWindowMissing = 0; // rows whose own date field is absent/unreadable -- dropped, see inDateWindow()

// The leading calendar date of whatever SAM.gov put in the field, or null if there isn't one.
function calDateOf(value) {
    if (value === null || value === undefined) return null;
    const m = /^(\d{4}-\d{2}-\d{2})/.exec(String(value));
    if (m) return m[1];
    // Defensive only: every normaliser in this file already emits ISO strings (normalizeWdRow runs
    // epoch ms through toIso), so this branch should not fire -- but a shape change upstream must
    // degrade to "unreadable date" and get the fail-closed treatment below, not to a silent keep.
    const d = new Date(String(value));
    return Number.isNaN(d.getTime()) ? null : d.toISOString().slice(0, 10);
}

// true = keep this row. Called on the NORMALISED item, so date shapes are already uniform.
// A row whose own date is missing or unreadable is DROPPED, not kept: we cannot prove it is inside
// the window the buyer paid to narrow to, and the whole point of a pre-charge filter is to never
// bill for a row we cannot stand behind. Counted separately from a real out-of-window drop so
// RUN_SUMMARY can distinguish "SAM.gov has lots of rows outside your window" from "SAM.gov served
// rows with no usable date", which are different problems with different fixes.
function inDateWindow(item) {
    if (!dateWindowActive) return true;
    for (const [from, to, field] of [[postedFrom, postedTo, 'publishDate'], [deadlineFrom, deadlineTo, 'responseDate']]) {
        if (!from && !to) continue;
        const d = calDateOf(item[field]);
        if (d === null) { dateWindowMissing += 1; return false; }
        if ((from && d < from) || (to && d > to)) { dateWindowDropped += 1; return false; }
    }
    return true;
}
function dateWindowText() {
    const parts = [];
    if (postedFrom || postedTo) parts.push(`posted ${postedFrom ?? 'any'}..${postedTo ?? 'any'}`);
    if (deadlineFrom || deadlineTo) parts.push(`deadline ${deadlineFrom ?? 'any'}..${deadlineTo ?? 'any'}`);
    return parts.join(', ');
}
// SOLICITATION NUMBER EXACT LOOKUP (cycle 2395; de-risked cycle 2394, see notes/LEARNINGS.md).
// `j0401`'s rival gap. SAM.gov's `solnum` query param does nothing -- probed live cycle 2394,
// confirmed silently dropped, not applied -- so like the date windows above this is a POST-FETCH
// filter: the value is sent as `q` to roughly scope the walk (there is no better server-side
// option), then any fetched row whose own `cleanSolicitationNumber` does not match is dropped
// before pushResult(). SAM.gov builds `cleanSolicitationNumber` by stripping every
// non-alphanumeric character from `solicitationNumber` (measured live: "SPRRA2-22-R-0016" ->
// "SPRRA222R0016") and matches it case-insensitively, so the input is normalised the same way --
// a buyer typing the number with or without dashes/spaces gets the same exact match. Sending the
// RAW value as `q` was measured to be WORSE, not just unnecessary: `q=SPRRA2-22-R-0016` (with
// dashes) returned a false-positive neighbour row ("APRRA2-22-R-0016", one letter off, total 4)
// that the cleaned form (`q=SPRRA222R0016`, total 3) does not, so the cleaned value is what is
// sent upstream.
const solicitationNumberRaw = String(input.solicitationNumber ?? '').trim();
let solicitationNumberClean = null;
if (solicitationNumberRaw) {
    solicitationNumberClean = solicitationNumberRaw.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
    if (!solicitationNumberClean) {
        await Actor.fail(
            `\`solicitationNumber\` ("${solicitationNumberRaw}") has no letters or digits once punctuation is `
            + 'stripped, so it can never exactly match a real solicitation number. Stopping before any request '
            + 'so you are charged nothing. Fix the value, or remove the field to search without it.',
        );
    }
}
const solicitationNumberActive = solicitationNumberClean !== null;
// Opportunities-index only -- wd/cfda/exclusions rows carry no solicitation number at all. A
// brand-new field gets the FAIL-CLOSED treatment (LEARNINGS cycle 2392 lesson 5), not the
// warn-and-ignore one naicsCodes/states get on those dataTypes: that behaviour predates paying
// buyers and cannot be changed now, whereas nothing depends on this field yet, so ignoring an
// unsupported combination here would bill the entire unfiltered set while looking narrowed.
if (solicitationNumberActive && (isWd || isCfda || isExclusions)) {
    await Actor.fail(
        `solicitationNumber is not supported for dataType "${dataType}": SAM.gov's "${dataType}" records carry no `
        + 'solicitation number field, so there is nothing to compare your value against. Stopping before any row '
        + 'is delivered or charged -- ignoring it would hand you every record matching your other filters, billed '
        + 'in full, while looking filtered. Use dataType "opportunities" for a solicitation-number lookup.',
    );
}
let solicitationNumberMismatch = 0; // fetched row carries a different solicitation number -- dropped, uncharged
let solicitationNumberMissing = 0;  // fetched row carries no solicitation number at all -- dropped, uncharged
function matchesSolicitationNumber(item) {
    if (!solicitationNumberActive) return true;
    const clean = item.cleanSolicitationNumber;
    if (!clean) { solicitationNumberMissing += 1; return false; }
    if (clean.toUpperCase() !== solicitationNumberClean) { solicitationNumberMismatch += 1; return false; }
    return true;
}
// NOTICE_ID FAST PATH (cycle 2397, scoped+probed cycle 2396 -- see notes/LEARNINGS.md). `notice_id`
// is a REAL server-side param on sgs/v1/search/ that -- despite its name -- matches the
// SOLICITATION NUMBER, not the 32-hex opportunity id: measured live, `notice_id=SPRRA2-22-R-0016`
// -> exactly 3 rows (the same amendment family the q=<clean> walk below finds by walking the whole
// index), AND-combines correctly with every other opp-index filter, and fails CLOSED on garbage
// (-> 0, never the unfiltered index). It is exact, case-SENSITIVE and wants the RAW punctuated
// form -- the cleaned/uppercased value this Actor sends as `q` (e.g. "SPRRA222R0016") returns 0
// against it -- so it cannot simply replace the q=<clean> walk below: a buyer typing lowercase or a
// different punctuation style would get nothing. Tried FIRST instead, with one `size=1` probe
// request (same zero-billable-rows shape as `assertFilterNamesApplied`'s canaries below): if the
// raw value matches, the real walk runs on notice_id instead of q and usually finishes in one
// page; if the probe returns 0 (wrong case, approximate input, or truly no match), fall back to
// the existing q=<clean> walk unchanged. The post-fetch exact filter (`matchesSolicitationNumber`)
// still runs on BOTH paths as the correctness guarantee -- notice_id being server-side is an
// efficiency win, not a reason to trust it unchecked. And because this endpoint fails OPEN (not
// closed) on a DROPPED filter NAME, `notice_id` is added to `guardedFilterNames()` below whenever
// this path is active, so a future silent SAM.gov change can't turn "1 exact row" into "the whole
// unfiltered index, billed in full" without the run erroring out first -- a `probeTotal > 0` check
// alone cannot tell "the value matched" apart from "the param was dropped and this is the index
// size", and 5,649,458 (this index's fail-open baseline, cycle 2396) would otherwise sail through
// the `> 0` check same as a real 1-row match.
let noticeIdFastPathActive = false;
if (solicitationNumberActive) {
    const probeParams = new URLSearchParams({
        index: 'opp', responseType: 'json', page: '0', size: '1',
        notice_id: solicitationNumberRaw,
    });
    const probeData = await apiGet(`${SEARCH_API}?${probeParams.toString()}`);
    const probeTotal = Number.isFinite(probeData?.page?.totalElements) ? Number(probeData.page.totalElements) : null;
    if (probeTotal !== null && probeTotal > 0) {
        noticeIdFastPathActive = true;
        log.info(`notice_id fast path: "${solicitationNumberRaw}" matched server-side (${probeTotal} row(s)); `
            + 'walking on notice_id instead of the full-text q=<clean> search.');
    } else {
        log.info(`notice_id fast path: "${solicitationNumberRaw}" did not match server-side (wrong case, `
            + 'approximate input, or no such notice); falling back to the q=<clean> full-text walk.');
    }
}

// AWARD AMOUNT RANGE (`tiger19935` rival gap, scoped c2396 -- see notes/LEARNINGS.md). Search rows
// already carry a full `award` object -- `award.amount` is a plain number, present (but null) on
// every non-award notice type and filled on award notices (`notice_type=a`) -- so, unlike the
// single-notice-by-id mode also scoped at c2396, this needs no detail call. SAM.gov's own
// `award_amount` query param is real but EXACT only (confirmed live: -> 55 rows, every one exactly
// 100000); every range syntax tried (`100000-200000`, `[100000 TO 200000]`, comma pairs, `>100000`)
// was rejected HTTP 400, and every from/to pair name (`award_amount_from`/`_to`/`_min`/`_max`) failed
// OPEN at the unfiltered count. So, same family as the date window and solicitationNumber above,
// this is a POST-FETCH range applied inside the fetch walk before pushResult().
async function awardAmountInput(name) {
    const raw = input[name];
    if (raw === undefined || raw === null || raw === '') return null;
    const n = Number(raw);
    // Fails CLOSED, not warn-and-ignore, per LEARNINGS c2392 lesson 5: this field is brand new
    // (nothing depends on it yet), so a value this Actor cannot apply must stop the run before any
    // row is fetched or charged -- ignoring it would hand back the whole unfiltered set, billed in
    // full, while looking narrowed to an award-value range.
    if (!Number.isFinite(n) || n < 0) {
        await Actor.fail(
            `\`${name}\` must be a non-negative number (a dollar amount, e.g. 100000), got "${raw}". Stopping before `
            + 'any row is delivered or charged. Fix the value, or remove the field to search without an award-amount range.',
        );
    }
    return n;
}
const minAwardAmount = await awardAmountInput('minAwardAmount');
const maxAwardAmount = await awardAmountInput('maxAwardAmount');
if (minAwardAmount !== null && maxAwardAmount !== null && minAwardAmount > maxAwardAmount) {
    await Actor.fail(
        `\`minAwardAmount\` (${minAwardAmount}) is GREATER than \`maxAwardAmount\` (${maxAwardAmount}), so the range `
        + 'is empty and this run could only ever return 0 rows no matter what SAM.gov holds. Swap the two values. '
        + 'Stopping before any request so you are charged nothing.',
    );
}
const awardAmountActive = minAwardAmount !== null || maxAwardAmount !== null;
// `award` only exists on the opportunities search-row shape (normalizeRow) -- wd/cfda/exclusions
// rows come from entirely different endpoints/normalisers and carry no award object at all, same
// unsupported-dataType shape as solicitationNumber above.
if (awardAmountActive && (isWd || isCfda || isExclusions)) {
    await Actor.fail(
        `minAwardAmount/maxAwardAmount ${minAwardAmount !== null && maxAwardAmount !== null ? 'are' : 'is'} not `
        + `supported for dataType "${dataType}": SAM.gov's "${dataType}" records carry no award-amount field at `
        + 'all, so there is nothing to compare your range against. Stopping before any row is delivered or charged '
        + '-- ignoring it would hand you every record matching your other filters, billed in full, while looking '
        + 'narrowed. Use dataType "opportunities" for an award-amount range.',
    );
}
if (awardAmountActive) {
    // `award.amount` is null by construction on every non-award notice type (presolicitation,
    // solicitation, etc. have not been awarded yet), so an award-amount range on a run that is not
    // already scoped to award notices will drop nearly everything as `awardAmountMissing` -- advisory
    // only, since a buyer may legitimately want "whatever few award rows a broad keyword turns up".
    if (!noticeTypes.length || !noticeTypes.every((t) => t === 'a')) {
        log.info('minAwardAmount/maxAwardAmount is set, but noticeTypes is not scoped to award notices only '
            + '("a") -- award.amount is null on every other notice type, so most fetched rows will be dropped as '
            + 'having no award amount to compare. Add noticeTypes: ["a"] to scope the walk to award notices only '
            + 'if that drop rate is not what you intended.');
    }
}
let awardAmountDropped = 0;  // fetched row's award.amount is outside the requested range -- dropped, uncharged
let awardAmountMissing = 0;  // fetched row has no award.amount at all (not yet awarded) -- dropped, uncharged
function inAwardAmountRange(item) {
    if (!awardAmountActive) return true;
    const amount = item.awardAmount;
    if (typeof amount !== 'number' || !Number.isFinite(amount)) { awardAmountMissing += 1; return false; }
    if ((minAwardAmount !== null && amount < minAwardAmount) || (maxAwardAmount !== null && amount > maxAwardAmount)) {
        awardAmountDropped += 1;
        return false;
    }
    return true;
}
function awardAmountText() {
    return `award amount $${(minAwardAmount ?? 0).toLocaleString('en-US')}..`
        + `${maxAwardAmount !== null ? `$${maxAwardAmount.toLocaleString('en-US')}` : 'any'}`;
}

// Shared by every site below that reconciles SAM's declared total against what this run actually
// delivered (same reconciliation requirement as the date window, LEARNINGS cycle 2392 lesson 2):
// every post-fetch filter drops fetched rows pre-charge, so all of them must be subtracted together
// or a run using any combination reports a false shortfall for working exactly as designed.
const postFetchFilterActive = dateWindowActive || solicitationNumberActive || awardAmountActive;
function postFetchFilterDroppedCount() {
    return dateWindowDropped + dateWindowMissing + solicitationNumberMismatch + solicitationNumberMissing
        + awardAmountDropped + awardAmountMissing;
}
function postFetchFilterText() {
    const parts = [];
    if (dateWindowActive) parts.push(`your date window (${dateWindowText()})`);
    if (solicitationNumberActive) parts.push(`solicitationNumber "${solicitationNumberRaw}"`);
    if (awardAmountActive) parts.push(`your ${awardAmountText()} range`);
    return parts.join(' and ');
}

let enrichDetail = input.enrichDetail === true;
let includeAttachments = input.includeAttachments === true;

// Filters that only exist on the opportunity index. Silently ignoring them in a wage-determination
// run would return a full 10,000-row unfiltered set that LOOKS filtered -- and every row is billed.
if (isWd) {
    const ignored = [];
    if (naicsCodes.length) ignored.push('naicsCodes');
    if (setAsideTypes.length) ignored.push('setAsideTypes');
    if (noticeTypes.length) ignored.push('noticeTypes');
    if (organizationId) ignored.push('organizationId');
    if (ignored.length) {
        log.warning(
            `${ignored.join(', ')} ${ignored.length === 1 ? 'is' : 'are'} only supported for dataType "opportunities" `
            + `and ${ignored.length === 1 ? 'was' : 'were'} IGNORED for "${dataType}". SAM.gov's wage-determination `
            + 'indices are filterable by state (`states`), active status (`activeOnly`) and reference-number keyword '
            + '(`keyword`) only -- your results are NOT narrowed by the ignored filter(s).',
        );
    }
    if (enrichDetail) {
        // Probed cycle 704: only CBA has a keyless per-record detail endpoint
        // (sam.gov/api/prod/wdol/v1/cba/<id>); the dbra/sca equivalents 404 on every guessed path.
        // Rather than enrich one of three modes asymmetrically, enrichment is opportunity-only.
        log.warning(`enrichDetail is only supported for dataType "opportunities"; ignored for "${dataType}".`);
        enrichDetail = false;
    }
    if (includeAttachments) {
        // Wage determinations are not notices and carry no attachment resources on this API.
        log.warning(`includeAttachments is only supported for dataType "opportunities"; ignored for "${dataType}".`);
        includeAttachments = false;
    }
}
// The cfda index shares `organization_id` with opportunities (confirmed live cycle 707:
// `organization_id=100000000` -> 189 programs, same param name), so it is NOT ignored here.
// `states`/`state` are confirmed NO-OPs on this index (both return the unfiltered 7,392 total --
// assistance-listing programs are nationwide, not place-of-performance filtered), so silently
// accepting them would look filtered while charging for the full unfiltered set.
if (isCfda) {
    const ignored = [];
    if (naicsCodes.length) ignored.push('naicsCodes');
    if (setAsideTypes.length) ignored.push('setAsideTypes');
    if (noticeTypes.length) ignored.push('noticeTypes');
    if (states.length) ignored.push('states');
    if (ignored.length) {
        log.warning(
            `${ignored.join(', ')} ${ignored.length === 1 ? 'is' : 'are'} only supported for dataType "opportunities" `
            + `and ${ignored.length === 1 ? 'was' : 'were'} IGNORED for "assistance-listings". SAM.gov's assistance-listing `
            + 'index is filterable by keyword (`keyword`, matches title/objective/program number), active status '
            + '(`activeOnly`) and organization (`organizationId`) only -- your results are NOT narrowed by the ignored filter(s).',
        );
    }
    if (enrichDetail) {
        // No keyless per-record detail endpoint probed for cfda (cycle 707) -- the search row
        // already carries the full record (financial/eligibility/contacts), so there is nothing a
        // detail call would add. Opportunity-only, same reasoning as the wd branch above.
        log.warning(`enrichDetail is only supported for dataType "opportunities"; ignored for "${dataType}".`);
        enrichDetail = false;
    }
    if (includeAttachments) {
        // Assistance-listing programs are not notices and carry no attachment resources on this API.
        log.warning(`includeAttachments is only supported for dataType "opportunities"; ignored for "${dataType}".`);
        includeAttachments = false;
    }
}
// `states` is confirmed APPLIED-BUT-FAILS-CLOSED on the exclusions index (`state=TX` -> 0 of
// 35,195, measured cycle 708/709, despite rows carrying `address.state`) -- silently accepting it
// would zero a buyer's result set with no explanation, so it is rejected outright rather than
// passed through like the other ignored filters. `organizationId` DOES work here (`organization_id`
// -> 41,843, same param as opportunities/cfda), so it is NOT ignored.
if (isExclusions) {
    const ignored = [];
    if (naicsCodes.length) ignored.push('naicsCodes');
    if (setAsideTypes.length) ignored.push('setAsideTypes');
    if (noticeTypes.length) ignored.push('noticeTypes');
    if (states.length) ignored.push('states');
    if (ignored.length) {
        log.warning(
            `${ignored.join(', ')} ${ignored.length === 1 ? 'is' : 'are'} only supported for dataType "opportunities" `
            + `and ${ignored.length === 1 ? 'was' : 'were'} IGNORED for "exclusions". SAM.gov's exclusions index is `
            + 'filterable by keyword (`keyword`, matches the entity name) and organization (`organizationId`) only -- '
            + 'your results are NOT narrowed by the ignored filter(s). `states` in particular is APPLIED but returns '
            + 'ZERO matches on this index no matter the value, so it is rejected here rather than silently zeroing your run.',
        );
    }
    // `activeOnly` is a silent NO-OP on this index -- measured live cycle 708/709: `is_active=true`
    // returns the same 35,195 total as no filter at all, even though every row carries a real
    // `isActive` boolean (fails OPEN, unlike `states` above which fails closed). Unlike the wd/cfda
    // indices, where activeOnly genuinely narrows the result, sending it here would look like it
    // filtered when it did nothing, so it is never sent to SAM.gov for this dataType and the buyer
    // is told once, plainly, regardless of the setting (activeOnly defaults to true).
    log.warning(
        'activeOnly has no effect on dataType "exclusions" -- SAM.gov\'s exclusions index does not support '
        + 'server-side active-status filtering (`is_active=true` returns the same total as no filter). Every '
        + 'exclusion record matching your other filters is returned regardless of this setting; check each row\'s '
        + 'own `isActive`/`terminationDate` fields if you need to filter locally.',
    );
    if (enrichDetail) {
        log.warning(`enrichDetail is only supported for dataType "opportunities"; ignored for "${dataType}".`);
        enrichDetail = false;
    }
    if (includeAttachments) {
        // Exclusion records are not notices and carry no attachment resources on this API.
        log.warning(`includeAttachments is only supported for dataType "opportunities"; ignored for "${dataType}".`);
        includeAttachments = false;
    }
}
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 200), 1), 10000); // 10k = confirmed backend depth cap (cycle 538)
const watchLabel = String(input.watchLabel ?? '').trim();
const watchChanges = Boolean(input.watchChanges);
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

if (solicitationNumberActive && keyword && keyword !== 'contract') {
    log.warning(
        `Both \`keyword\` ("${keyword}") and \`solicitationNumber\` were given; solicitationNumber takes over the `
        + 'search query (sent to SAM.gov as `q`) because an exact solicitation-number match narrows better than a '
        + 'keyword, and `keyword` is ignored for this run\'s SAM.gov request. The result is still an exact match '
        + 'on solicitationNumber regardless of this.',
    );
}

log.info(`Starting SAM.gov ${ROW_NOUN} search (dataType=${dataType}, index=${SEARCH_INDEX})`, {
    keyword, naicsCodes, setAsideTypes, noticeTypes, states, organizationId, activeOnly, maxResults, enrichDetail, includeAttachments, watchLabel,
    // Echoed only when set, so the window/lookup is visible in the run log from line one -- both
    // are filters applied client-side, and a buyer debugging "why so few rows?" should see them
    // stated next to the server-side filters rather than inferred from the Done line.
    ...(dateWindowActive ? { postedFrom, postedTo, deadlineFrom, deadlineTo } : {}),
    ...(solicitationNumberActive ? { solicitationNumber: solicitationNumberClean, noticeIdFastPath: noticeIdFastPathActive } : {}),
});

function buildSearchUrl(page, size) {
    if (isExclusions) {
        const params = new URLSearchParams({
            index: SEARCH_INDEX, responseType: 'json',
            page: String(page), size: String(size),
            // MANDATORY, NON-NEGOTIABLE (CLAUDE.md rule 1 / cycle 708 finding). 133,478 of the
            // 168,673 rows on this index (79%) are `classification.code: "Individual"` -- a named
            // private person with a home city/state/zip. Shipping those would be a PII-harvesting
            // product. This param is hard-coded into the REQUEST -- never fetch-then-filter, which
            // would still pull and briefly hold the person rows -- and there is no input anywhere
            // in this Actor that can widen or remove it. Verified live (cycle 708/709): the four
            // classification values partition the index exactly to the row (Individual 133,478 +
            // Special Entity Designation 25,586 + Firm 8,287 + Vessel 1,322 = 168,673), comma-join
            // is a true OR (`Firm,Vessel` -> 9,609 = 8,287+1,322), and an unrecognised value fails
            // CLOSED (`classification=Nonsense` -> 0) -- so this is safe to rely on, not a
            // coincidence of the current data.
            classification: 'Firm,Vessel,Special Entity Designation',
        });
        if (keyword) params.set('q', keyword);
        if (organizationId) params.set('organization_id', organizationId);
        return `${SEARCH_API}?${params.toString()}`;
    }
    if (isWd) {
        const params = new URLSearchParams({
            index: SEARCH_INDEX, responseType: 'json',
            page: String(page), size: String(size),
        });
        if (keyword) params.set('q', keyword);
        if (activeOnly) params.set('is_active', 'true');
        // The state param is `state`, NOT the opportunity index's `pop_state` -- measured live
        // cycle 704: `state=AL` -> 3,509 and `state=TX` -> 6,909 on index=wd, while `pop_state=AL`
        // returns 0 (applied, matches nothing) and an unrecognised name like `wd_state=AL` returns
        // the unfiltered 107,580. Comma-join is a true OR, same as the opportunity filters:
        // `state=AL,TX` -> 10,415, i.e. 3,509 + 6,909 minus the 3 determinations covering both;
        // repeating the key (`state=AL&state=TX`) first-wins at 3,509 and fails OPEN, so never do it.
        if (states.length) params.set('state', states.join(','));
        return `${SEARCH_API}?${params.toString()}`;
    }
    if (isCfda) {
        const params = new URLSearchParams({
            index: SEARCH_INDEX, responseType: 'json',
            page: String(page), size: String(size),
        });
        if (keyword) params.set('q', keyword);
        if (activeOnly) params.set('is_active', 'true');
        if (organizationId) params.set('organization_id', organizationId);
        return `${SEARCH_API}?${params.toString()}`;
    }
    // `mode=search` truncates `descriptions[0].content` to 250 chars server-side -- confirmed by
    // diffing identical queries with/without it (cycle 567): same `totalElements`, same row ids
    // per page (intra-page order can differ on relevance ties, never drops/adds a row), but content
    // length caps at exactly 250 with the param and runs up to 37k+ chars without it. Omitting it
    // is a zero-new-request way to deliver the FULL solicitation description text.
    const params = new URLSearchParams({
        index: 'opp', responseType: 'json',
        page: String(page), size: String(size),
    });
    // solicitationNumber takes over `q` entirely when set -- it is a full-text match that scopes
    // the walk far better than the default "contract" keyword, and correctness is guaranteed by
    // the exact post-fetch filter below regardless of what `q` returns (same reasoning
    // `assertFilterNamesApplied` already uses to exclude `q` from the dropped-filter-name canary).
    // When the notice_id probe above found this exact raw value server-side, use that instead of
    // `q` -- it is EXACT (no false-positive neighbours, unlike the q=<clean> full-text match) and
    // usually ends the walk in one page. `matchesSolicitationNumber` still runs on every row either
    // way, so a (currently unobserved) notice_id false positive would still be caught and dropped.
    if (noticeIdFastPathActive) params.set('notice_id', solicitationNumberRaw);
    else if (solicitationNumberActive) params.set('q', solicitationNumberClean);
    else if (keyword) params.set('q', keyword);
    if (activeOnly) params.set('is_active', 'true');
    if (organizationId) params.set('organization_id', organizationId);
    // Multi-value params must be COMMA-JOINED, not repeated. Measured live cycle 540 by
    // result-count arithmetic: `naics=541511`->607 and `naics=541512`->312, but repeating the key
    // (`naics=541511&naics=541512`) returns 607 -- silently first-wins, dropping the rest -- while
    // `naics=541511,541512` returns exactly 919 = 607+312, a true OR. Same confirmed for
    // pop_state (TX 592 + CA 767 = TX,CA 1359) and notice_type (p 4016 + o 8281 = p,o 12297).
    // Repeating the key fails OPEN (plausible-looking under-count, no error), so never go back.
    if (naicsCodes.length) params.set('naics', naicsCodes.join(','));
    if (setAsideTypes.length) params.set('set_aside', setAsideTypes.join(','));
    if (noticeTypes.length) params.set('notice_type', noticeTypes.join(','));
    if (states.length) params.set('pop_state', states.join(','));
    return `${SEARCH_API}?${params.toString()}`;
}

// SAM.gov fails CLOSED on an unrecognised filter VALUE but fails OPEN on an unrecognised filter
// NAME -- the name is silently dropped and the query returns the WHOLE index at the same HTTP 200.
// Measured live cycle 748 on index=opp: `naics=541511` -> 604 matches, the one-letter typo
// `naic=541511` -> 52,460. That is an 86x widening, and under per-result pricing every one of those
// rows would be pushed and CHARGED as a real match.
// The `_links.self.href` echo cannot detect this: it echoes the REQUEST verbatim, so a dropped
// param still appears in it (verified -- `naic=541511` is echoed back unchanged). That is the
// difference from grants-gov's `data.searchParams`, which echoes only the PARSED params and so
// supports a round-trip assertion (cycle 744) -- the same guard shape does NOT port here.
// The worst case is not the over-bill, it is index=ei: the hard-coded `classification` PII gate in
// `buildSearchUrl` above is the only thing keeping named private individuals out of the output, and
// it is exactly as droppable. Measured live: `classification=Firm,Vessel,Special Entity Designation`
// -> 35,206 rows, `classificatio=...` (one letter short) -> 168,689 = the full index, INCLUDING all
// 133,483 `Individual` person rows with their home city/state/zip. The cycle 708 note above only
// established that a bad VALUE fails closed; the dropped-NAME case was never checked until now.
// The guard below sends each filter name we are about to use with a value that cannot match
// anything: a recognised name fails closed -> 0 matches, a dropped name returns the full index -> >0.
// Deterministic and false-positive-free (it never depends on the user's real filter values), and it
// costs one `size=1` request per distinct filter name -- zero billable rows.
const FILTER_CANARY = '__fetchsmith_canary_no_such_value__';

function guardedFilterNames() {
    const names = [];
    if (isExclusions) {
        names.push('classification'); // mandatory PII gate -- probed on EVERY run, user filters or not
        if (organizationId) names.push('organization_id');
    } else if (isWd) {
        // Verified live cycle 748 on all three wd-family indices (dbra/sca/wd): `state=<canary>`
        // returns 0 on each, so this probe is safe on every index the family can select.
        if (states.length) names.push('state');
    } else if (isCfda) {
        if (organizationId) names.push('organization_id');
    } else {
        if (naicsCodes.length) names.push('naics');
        if (setAsideTypes.length) names.push('set_aside');
        if (noticeTypes.length) names.push('notice_type');
        if (states.length) names.push('pop_state');
        if (organizationId) names.push('organization_id');
        // Guarded only when this run actually relies on it (`noticeIdFastPathActive`), same
        // condition that put it in buildSearchUrl -- measured cycle 2396 to fail CLOSED on a
        // non-matching value, so FILTER_CANARY is a valid probe for it, same as every other name
        // in this branch.
        if (noticeIdFastPathActive) names.push('notice_id');
    }
    // `is_active` and `q` are deliberately NOT probed. `is_active=<canary>` returns HTTP 400 (it is
    // parsed as a boolean, so a non-boolean value cannot be used as a canary -- measured cycle 748),
    // and a keyword that matches nothing is a legitimate `q` result, not evidence the name was kept.
    return names;
}

async function assertFilterNamesApplied() {
    for (const name of guardedFilterNames()) {
        const params = new URLSearchParams({
            index: SEARCH_INDEX, responseType: 'json', page: '0', size: '1',
        });
        params.set(name, FILTER_CANARY);
        const data = await apiGet(`${SEARCH_API}?${params.toString()}`);
        const total = Number.isFinite(data?.page?.totalElements) ? Number(data.page.totalElements) : null;
        if (total === null) {
            // An upstream blip is not evidence of a dropped filter -- do not fail the run on it.
            log.warning(`Could not verify that SAM.gov still honours the "${name}" filter `
                + `(probe request failed: ${lastApiError ?? 'no usable total in response'}); continuing.`);
            continue;
        }
        if (total > 0) {
            throw new Error(
                `SAM.gov no longer recognises the "${name}" search filter: a probe request with `
                + `${name}=${FILTER_CANARY} returned ${total} matches instead of 0, which means the `
                + `parameter is now being silently ignored and this search would return the entire `
                + `"${SEARCH_INDEX}" index instead of your filtered subset`
                + (isExclusions ? ', including the individual-person rows this Actor never publishes' : '')
                + '. Stopping before any unfiltered rows are delivered or charged. This is an upstream '
                + 'SAM.gov API change -- please report it so the Actor can be updated.',
            );
        }
        log.info(`Verified SAM.gov still honours the "${name}" filter (canary value returned 0 matches).`);
    }
}

function orgField(hierarchy, type) {
    const row = (hierarchy ?? []).find((h) => h.type === type);
    return row ? row.name : null;
}

function normalizeRow(row) {
    const id = row._id;
    return {
        opportunityId: id,
        title: row.title ?? null,
        solicitationNumber: row.solicitationNumber ?? null,
        // SAM.gov's own punctuation-stripped form of solicitationNumber (e.g. "SPRRA2-22-R-0016"
        // -> "SPRRA222R0016", measured live cycle 2395) -- what `solicitationNumber` input below
        // is matched against, so a buyer sees exactly the value the exact-match filter compared.
        cleanSolicitationNumber: row.cleanSolicitationNumber ?? null,
        noticeTypeCode: row.type?.code ?? null,
        noticeType: row.type?.value ?? null,
        isActive: row.isActive ?? null,
        isCanceled: row.isCanceled ?? null,
        publishDate: row.publishDate ?? null,
        modifiedDate: row.modifiedDate ?? null,
        responseDate: row.responseDate ?? null,
        responseDateActual: row.responseDateActual ?? null,
        responseTimeZone: row.responseTimeZone ?? null,
        department: orgField(row.organizationHierarchy, 'DEPARTMENT'),
        agency: orgField(row.organizationHierarchy, 'AGENCY'),
        office: orgField(row.organizationHierarchy, 'OFFICE'),
        description: row.descriptions?.[0]?.content ?? null,
        awardeeName: row.award?.awardee?.name ?? null,
        awardeeUeiSAM: row.award?.awardee?.ueiSAM ?? null,
        // Plain number on award notices (`notice_type=a`), null on every other notice type -- not
        // yet awarded. Powers the minAwardAmount/maxAwardAmount post-fetch range below.
        awardAmount: typeof row.award?.amount === 'number' ? row.award.amount : null,
        modificationsCount: row.modifications?.count ?? 0,
        sourceUrl: id ? `https://sam.gov/opp/${id}/view` : null,
        // Detail-only fields, filled in only when enrichDetail is on (extra HTTP call per row).
        naicsCodes: null,
        setAside: null,
        placeOfPerformanceState: null,
        placeOfPerformanceCountry: null,
        pointOfContact: null,
        // Attachment list, filled in only when includeAttachments is on (extra HTTP call per row).
        attachments: null,
    };
}

// The three wage-determination indices describe the same thing in three different location shapes,
// all confirmed against live rows (cycle 704):
//   wdDBRA  location.state  = { code, name, counties: [{code, value}] }      (singular object)
//   wdCBA   location.states = [{ code, name, counties: [{code, value}] }]    (array)
//   wdSCA   location.states = [{ code, name, isStateWide, counties: { include: [...], exclude: [...] } }]
// Flattened to one `coverage` array so a buyer writes one parser, not three. SCA's `exclude` list is
// kept as its own field rather than folded into the county list -- an excluded county is the exact
// opposite of a covered one, and silently merging them would be a wrong answer, not a lossy one.
function countyNames(counties) {
    if (Array.isArray(counties)) return counties.map((c) => c?.value ?? null).filter(Boolean);
    if (Array.isArray(counties?.include)) return counties.include.map((c) => c?.value ?? null).filter(Boolean);
    return [];
}
function excludedCountyNames(counties) {
    return Array.isArray(counties?.exclude) ? counties.exclude.map((c) => c?.value ?? null).filter(Boolean) : [];
}
function coverageOf(location) {
    const states = Array.isArray(location?.states) ? location.states : (location?.state ? [location.state] : []);
    return states.map((s) => ({
        stateCode: s?.code ?? null,
        stateName: s?.name ?? null,
        isStateWide: s?.isStateWide ?? null,
        counties: countyNames(s?.counties),
        excludedCounties: excludedCountyNames(s?.counties),
    }));
}

// `publishDate` comes back as an ISO string on wdCBA but as epoch MILLISECONDS on wdDBRA/wdSCA
// (measured live cycle 704: 1789617600000). Emitting both shapes under one field name would make
// every downstream date parse a coin flip, so normalise to ISO here.
function toIso(value) {
    if (value === null || value === undefined) return null;
    if (typeof value === 'number') return new Date(value).toISOString();
    return String(value);
}

function normalizeWdRow(row) {
    const id = row._id;
    const coverage = coverageOf(row.location);
    return {
        wageDeterminationId: id === null || id === undefined ? null : String(id),
        // wdDBRA/wdSCA carry `fullReferenceNumber` (e.g. "AK20260001", "2014-0333"); wdCBA carries
        // `cbaNumber` (e.g. "CBA-2003-2"). `title` mirrors whichever exists on all three.
        referenceNumber: row.fullReferenceNumber ?? row.cbaNumber ?? row.title ?? null,
        shortReferenceNumber: row.shortReferenceNumber ?? null,
        title: row.title ?? null,
        actCode: row.type?.code ?? null,       // DBA | SCA | CBA
        actName: row.type?.value ?? null,      // Davis-Bacon Act | Service Contract Act | Collective Bargaining Agreement
        recordType: row._type ?? null,         // wdDBRA | wdSCA | wdCBA
        isActive: row.isActive ?? null,
        isLatest: row.isLatest ?? null,
        isStandard: row.isStandard ?? null,
        revisionNumber: typeof row.revisionNumber === 'number' ? row.revisionNumber : null,
        year: typeof row.year === 'number' ? row.year : null,
        publishDate: toIso(row.publishDate),
        modifiedDate: toIso(row.modifiedDate),
        // DBRA only: which kinds of construction the schedule applies to (Building/Heavy/Highway/
        // Residential). SCA only: the service categories it covers.
        constructionTypes: Array.isArray(row.constructionTypes) ? row.constructionTypes : null,
        services: Array.isArray(row.services)
            ? row.services.map((s) => ({ code: s?.code ?? null, name: s?.value ?? null, description: s?.description ?? null }))
            : null,
        coverage,
        stateCodes: coverage.map((c) => c.stateCode).filter(Boolean),
        countyCount: coverage.reduce((n, c) => n + c.counties.length, 0),
        // Per-occupation wage RATE schedules are not on the search row for any of the three
        // indices, and only wdCBA has a keyless per-record detail endpoint (cycle 704), so this
        // Actor delivers the determination index -- which determination applies where, and whether
        // it is current -- not the rate tables. Said plainly here and in the README so nobody buys
        // rows expecting hourly rates.
        wageRates: null,
    };
}

// cfda's organizationHierarchy entries carry NO `type` field (unlike opp's, which orgField()
// above reads) -- only `level` (1 = department, 2 = agency, checked live cycle 707 against real
// records; a 3rd level was never observed in samples but the accessor stays general). Do NOT
// reuse orgField() for cfda rows -- it would silently return null for every one of them.
function orgFieldByLevel(hierarchy, level) {
    const row = (hierarchy ?? []).find((h) => h.level === level);
    return row ? row.name : null;
}

// CFDA (Catalog of Federal Domestic Assistance) rows describe grant/loan/direct-payment programs,
// a structurally richer family than opp/wd -- confirmed live cycle 707. `_id` is a stable 32-char
// hex id (same role as opp's `_id`). `programNumber` (e.g. "12.103") is the reference number
// buyers actually search by, same role as wd's `referenceNumber`. `publishDate`/`modifiedDate` are
// ISO strings on every sample checked (unlike wd's epoch-ms DBRA/SCA split) -- no toIso() needed.
// `contacts` is the agency's own published program contact, same PII-safe reasoning already
// applied to opp's `pointOfContact` (statutory public notice, not a person's private profile).
// `financial.obligations` is shipped as raw pass-through, not normalized. Cycle 707 deferred the
// flag-vocabulary question (one sample read had only a `flag`, no numeric amount); cycle 1988 CLOSED
// it by reading the whole catalog (7,396 programs / 74 pages / 32s / no key, keyless hal+json).
// Corrected findings -- the 707 sample was NOT representative:
//   * value-entry keys: year 16594, actual 9432, estimate 8019, flag 1036 (only 6.2%), explanation 403
//   * flag vocabulary is EXACTLY two: `ena` (696, estimate not available), `nsi` (340, not separately
//     identifiable -- money booked under another programNumber, named in `explanation`)
//   * amounts are mostly present: 4205 programs have a non-empty block, 4093 of those (97.3%) carry
//     a real number; only 77 are flag-only. So "the amounts are missing" was wrong.
// Raw pass-through still stands, for a STRONGER reason: any single normalized amount field would be
// silently wrong on >1/3 of entries. `0` is a placeholder not a quantity (2943 estimate=0 + 2737
// actual=0 = 34.2% of entries; e.g. 10.856 FY2013 = {flag:"ena", estimate:0, explanation:"Program
// not funded"}), and `estimate`/`actual` CO-OCCUR on 1771 entries and disagree by up to ~50%
// (14.880 FY2019: estimate 20.0M vs actual 29.967M) -- there is no single "the amount" to pick.
// Do not add a normalized amount field without a caller-chosen actual-vs-estimate preference.
// Measured: site/content/blog/cfda-funding-history-zero-is-not-zero.md
function normalizeCfdaRow(row) {
    const id = row._id;
    return {
        assistanceListingId: id === null || id === undefined ? null : String(id),
        programNumber: row.programNumber ?? null,
        title: row.title ?? null,
        alternativeNames: Array.isArray(row.alternativeNames) ? row.alternativeNames : null,
        objective: row.objective ?? null,
        isActive: row.isActive ?? null,
        isFunded: row.isFunded ?? null,
        isLatest: row.isLatest ?? null,
        publishDate: row.publishDate ?? null,
        modifiedDate: row.modifiedDate ?? null,
        department: orgFieldByLevel(row.organizationHierarchy, 1),
        agency: orgFieldByLevel(row.organizationHierarchy, 2),
        assistanceTypes: Array.isArray(row.assistanceTypes)
            ? row.assistanceTypes.map((t) => (t?.hierarchy ?? []).map((h) => h?.value ?? null).filter(Boolean))
            : null,
        eligibleApplicants: row.eligibility?.applicant?.types?.map((t) => t?.value ?? null).filter(Boolean) ?? null,
        eligibleApplicantsNote: row.eligibility?.applicant?.additionalInfo ?? null,
        eligibleBeneficiaries: row.eligibility?.beneficiary?.types?.map((t) => t?.value ?? null).filter(Boolean) ?? null,
        eligibleBeneficiariesNote: row.eligibility?.beneficiary?.additionalInfo ?? null,
        obligations: Array.isArray(row.financial?.obligations) ? row.financial.obligations : null,
        contacts: Array.isArray(row.contacts)
            ? row.contacts.map((c) => ({ name: c?.name ?? null, title: c?.title ?? null, phone: c?.phone ?? null, address: c?.address?.streetAddress ?? null }))
            : null,
        relatedPrograms: Array.isArray(row.relatedPrograms) ? row.relatedPrograms.map((p) => p?.programNumber ?? null).filter(Boolean) : null,
        website: row.website ?? null,
        historicalIndexCount: Array.isArray(row.historicalIndex) ? row.historicalIndex.length : null,
        sourceUrl: id ? `https://sam.gov/fal/${id}/view` : null,
    };
}

// Exclusions (federal debarment/suspension list). `organizationHierarchy` here goes 3 levels deep
// (1=department, 2=agency, 3=office -- confirmed live cycle 709, one level deeper than cfda's
// department/agency pair), so `orgFieldByLevel()` above is reused rather than duplicated.
// `activationDate`/`terminationDate` are plain date strings or null on every sampled row (no
// epoch-ms split like wdDBRA/wdSCA had -- checked live, not assumed, per cycle 704's lesson).
// `noPublicDisplayFlag` is normalized to a boolean here; the raw row is checked for `"T"` and the
// row dropped entirely BEFORE it reaches this function (see the fetch loop) -- SAM.gov's own
// do-not-display marker overrides classification, so a Firm/Vessel/SED row can still be withheld.
function normalizeExclusionRow(row) {
    const id = row._id;
    return {
        exclusionId: id === null || id === undefined ? null : String(id),
        title: row.title ?? null,
        classificationCode: row.classification?.code ?? null,
        ueiSam: row.ueiSam ?? null,
        cageCode: row.cageCode ?? null,
        samNumber: row.samNumber ?? null,
        addressCity: row.address?.city ?? null,
        addressState: row.address?.state ?? null,
        addressCountry: row.address?.country ?? null,
        addressZip: row.address?.zip ?? null,
        exclusionTypeCode: row.type?.code ?? null,
        exclusionType: row.exclusionType ?? row.type?.value ?? null,
        exclusionProgram: row.exclusionProgram ?? null,
        excludingAgency: row.excludingAgency ?? null,
        excludingAgencyDesc: row.excludingAgencyDesc ?? null,
        department: orgFieldByLevel(row.organizationHierarchy, 1),
        agency: orgFieldByLevel(row.organizationHierarchy, 2),
        office: orgFieldByLevel(row.organizationHierarchy, 3),
        isActive: row.isActive ?? null,
        activationDate: row.activationDate ?? null,
        terminationDate: row.terminationDate ?? null,
        isFascsaOrder: row.isFascsaOrder ?? null,
        sourceUrl: id ? `https://sam.gov/exclusion/${id}/view` : null,
    };
}

// One identity accessor for all four row shapes, so the dedupe set, the watch baseline and the
// push loop can never disagree about what "the id of this row" means.
function idOf(item) {
    return item.opportunityId ?? item.wageDeterminationId ?? item.assistanceListingId ?? item.exclusionId ?? null;
}

let detailLookupsFailed = 0;
let attachmentLookupsFailed = 0;

// A notice with no files at all is common and real (most presolicitations and many award
// notices have none) -- that is `attachments: []`, not a failure. A failed lookup leaves
// `attachments: null` instead, same "null means the call broke, not that the answer is empty"
// rule as enrichDetail's fields, so a buyer can tell the two apart from the row alone.
async function fetchAttachments(item) {
    if (!item.opportunityId) { item.attachments = null; return item; }
    const resp = await apiGet(`${ATTACHMENTS_API}/${item.opportunityId}/resources`);
    if (!resp) { attachmentLookupsFailed += 1; item.attachments = null; return item; }
    // A notice with zero attachments omits `_embedded` entirely rather than returning an empty
    // list under it (verified live cycle 1133 against several sources-sought notices) -- `resp`
    // being a real, non-null response with no `_embedded` key IS the genuine "no files" answer.
    const list = resp._embedded?.opportunityAttachmentList?.[0]?.attachments ?? [];
    item.attachments = list
        // `deletedFlag`/`fileExists` filter out resources SAM.gov still lists but no longer serves.
        // `accessLevel !== 'public'` (export-controlled or explicit-access files) is excluded too --
        // this Actor publishes no-login public links only, never a URL that would 403/redirect to
        // a SAM.gov sign-in for the buyer.
        .filter((a) => a.deletedFlag !== '1' && a.fileExists !== '0' && a.accessLevel === 'public')
        .map((a) => ({
            name: a.name ?? null,
            mimeType: a.mimeType ?? null,
            sizeBytes: typeof a.size === 'number' ? a.size : null,
            postedDate: a.postedDate ?? null,
            downloadUrl: a.resourceId ? attachmentDownloadUrl(a.resourceId) : null,
        }));
    return item;
}

async function enrichOne(item) {
    if (!item.opportunityId) return item;
    const detail = await apiGet(`${DETAIL_API}/${item.opportunityId}`);
    if (!detail?.data2) { detailLookupsFailed += 1; return item; }
    const d = detail.data2;
    item.naicsCodes = Array.isArray(d.naics) ? d.naics.flatMap((n) => n.code ?? []) : null;
    item.setAside = d.solicitation?.setAside ?? d.award?.setAside ?? null;
    item.placeOfPerformanceState = d.placeOfPerformance?.state?.code ?? null;
    item.placeOfPerformanceCountry = d.placeOfPerformance?.country?.code ?? null;
    // Government office contacts, published by the agency itself as part of the statutory
    // public notice (same disclosure class already reviewed for nih-reporter-scraper /
    // eu-ted-tenders-scraper) -- not scraped from a person's private profile, not aggregated
    // across sources, not resold as a people-lookup product. PII-safe to include as-is.
    item.pointOfContact = Array.isArray(d.pointOfContact)
        ? d.pointOfContact.map((c) => ({ name: c.fullName ?? null, email: c.email ?? null, phone: c.phone ?? null, type: c.type ?? null }))
        : null;
    return item;
}

// ---------------------------------------------------------------------------
// Watch mode: "only what is new since my last run", per saved query. Same shape as
// grants-gov-scraper/federal-register-scraper (cycle 297+) -- copy that design, don't reinvent it.
//
// The baseline is the buyer's own -- the opportunity ids this label has already delivered -- kept
// in a NAMED key-value store so it survives across runs (the default per-run KV store would reset
// the baseline every run, i.e. re-charge the whole result set every time). `opportunityId` (SAM's
// `_id`) is the stable identity: it's what the detail endpoint and the public /opp/<id>/view URL
// key off, whereas `solicitationNumber` is an agency-entered label that can in principle repeat.
const WATCH_STORE = 'fetchsmith-samgov-watch';
const SEED_CAP = 10000; // same as SAM.gov's own hard backend depth cap -- a seed walk can never
// need to go deeper than the platform itself allows for one query.
const WATCH_KEEP = 60000; // bound the KV record size; oldest ids fall off first

const watchMode = watchLabel.length > 0;

// Apify KV keys allow [a-zA-Z0-9!-_.'()] only, so the label is sanitised rather than trusted. The
// criteria fingerprint is part of the key on purpose: if the buyer edits a filter, that's a
// different question and gets its own baseline, instead of dumping every opportunity the old
// narrower filter happened to exclude as if it were brand new. `enrichDetail` is deliberately left
// out -- it changes output richness, not which opportunities match, same reasoning as `enrich` on
// grants-gov-scraper's watchCriteria.
function watchKeyFor(label, criteria) {
    const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
    const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
    return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const watchCriteria = {
    // dataType is part of the fingerprint: opportunities and wage determinations are different
    // questions with disjoint id spaces, so they must never share a baseline.
    dataType,
    keyword, naicsCodes: [...naicsCodes].sort(), setAsideTypes: [...setAsideTypes].sort(),
    noticeTypes: [...noticeTypes].sort(), states: [...states].sort(), organizationId, activeOnly,
    // The date windows belong in the fingerprint for the same reason every other filter does:
    // they change WHICH rows match, so widening one must start a fresh baseline instead of
    // dumping every row the narrower window excluded as if it were brand new (cycle 2392).
    postedFrom, postedTo, deadlineFrom, deadlineTo,
    // Same reasoning: a solicitation-number lookup changes WHICH rows match, so changing it (or
    // clearing it) must start a fresh baseline rather than dumping every previously-excluded row.
    solicitationNumber: solicitationNumberClean,
    // Same reasoning again: an award-amount range changes WHICH rows match.
    minAwardAmount, maxAwardAmount,
};

// Snapshot of the fields that can change on an already-delivered opportunity: `isActive`/
// `noticeTypeCode` (the presolicitation -> solicitation -> award lifecycle transition SAM.gov's
// own demand data flags as the single most valuable alert in this niche), `responseDate` (a
// deadline extension -- the highest-frequency real change), `modifiedDate` (SAM's own "this
// notice was edited" stamp), `modificationsCount` and `awardeeName` (null -> set is the award
// landing). `description` is now the FULL solicitation text (cycle 567, can run 10k+ chars) -- the
// fleet rule is never to store free text in a watch snapshot, so only an 8-char md5 fingerprint of
// it is kept, enough to detect an edit without risking the KV record's size budget (WATCH_KEEP
// holds up to 60,000 of these).
function descHashOf(desc) {
    return desc ? createHash('md5').update(desc).digest('hex').slice(0, 8) : null;
}
const WATCHED_FIELDS_TEXT = isExclusions
    ? 'active status or termination date'
    : isCfda
    ? 'active or funded status, modified date, or historical-index entry count'
    : isWd
    ? 'revision number, active status or modified date'
    : 'active/notice-type status, response deadline, modified date, modification count, awardee or description';

function snapshotOf(item) {
    return {
        isActive: item.isActive ?? null,
        noticeTypeCode: item.noticeTypeCode ?? null,
        responseDate: item.responseDate ?? null,
        modifiedDate: item.modifiedDate ?? null,
        modificationsCount: typeof item.modificationsCount === 'number' ? item.modificationsCount : null,
        awardeeName: item.awardeeName ?? null,
        descHash: descHashOf(item.description),
        // Wage determinations have no notice lifecycle or response deadline; what moves on them is
        // a REVISION (Davis-Bacon schedules are revised many times a year) and isActive flipping
        // when a newer revision supersedes them. Always null on an opportunity row.
        revisionNumber: typeof item.revisionNumber === 'number' ? item.revisionNumber : null,
        // Assistance listings have no revision number either; what moves is funded status
        // (isFunded flips as budgets are appropriated) and the historical-index log growing when
        // SAM.gov records a title/agency change (not yet observed live over time as of cycle 707 --
        // treated as a candidate signal, not a confirmed one; harmless if it never fires). Always
        // null on an opp/wd row.
        isFunded: typeof item.isFunded === 'boolean' ? item.isFunded : null,
        historicalIndexCount: typeof item.historicalIndexCount === 'number' ? item.historicalIndexCount : null,
        // Exclusions have no notice lifecycle, revision or funded flag either; what moves is a
        // debarment being LIFTED (`terminationDate` going from null to set, `isActive` flipping to
        // false). Always null on an opp/wd/cfda row.
        terminationDate: item.terminationDate ?? null,
    };
}

// A changed opportunity is re-delivered tagged with exactly what moved, so a buyer doesn't have to
// diff the row against their own last-seen copy to find out. descHash is compared separately since
// its "previous" value (a hash) isn't meaningful to show a buyer.
function changesBetween(prev, next) {
    if (!prev) return null;
    const types = [];
    const previous = {};
    for (const field of ['isActive', 'noticeTypeCode', 'responseDate', 'modifiedDate', 'modificationsCount', 'awardeeName', 'revisionNumber', 'isFunded', 'historicalIndexCount', 'terminationDate']) {
        if (prev[field] !== undefined && prev[field] !== null && prev[field] !== next[field]) {
            types.push(field);
            previous[field] = prev[field];
        }
    }
    if (prev.descHash !== undefined && prev.descHash !== null && prev.descHash !== next.descHash) {
        types.push('description');
        previous.description = '(changed; only a fingerprint of the description is retained, not the previous text)';
    }
    return types.length ? { types, previous } : null;
}

// Change-blind filters (cycle 1560/1561/1567; same class as grants-gov-scraper c860 /
// clinicaltrials-scraper c861 / fda-recall-scraper c1560 / trademark-search-scraper c1561).
// Two independent instances here, confirmed live against real sam.gov rows (cycle 1567, naics
// 221122: a real id -- 25e3e2d15abd0a52d90c53a58e166484 -- with isActive:false present in the
// unfiltered result set and absent from the is_active=true one). `isActive` is snapshotOf()'s
// #1 watched field (the active -> inactive/awarded transition is the single most valuable alert
// in this niche per the comment above snapshotOf), and `activeOnly` sends that exact field to
// SAM.gov as the server-side `is_active=true` filter on every index except exclusions (already a
// documented no-op there, not a filter -- see the warning above). The moment a row flips inactive,
// `is_active=true` stops returning it at all, so changesBetween() is never called and the
// transition is never reported -- the run just says nothing was new. UNLIKE the other four
// instances, `activeOnly` DEFAULTS TO TRUE: this fires on the DEFAULT setting, not just when a
// buyer opts into a filter, so most watchChanges runs on this Actor are blind to it already.
// `noticeTypes` (opportunities dataType only) is a second, narrower instance: sent as
// `notice_type`, and `noticeTypeCode` is watched for the presolicitation -> solicitation -> award
// lifecycle -- filtering to one notice type blinds the transition out of that type, same shape as
// TMview's `statuses` at c1561. Advisory only for noticeTypes (defaults empty).
const watchChangeBlindFilters = [];
if (watchMode && watchChanges) {
    if (activeOnly && !isExclusions) {
        watchChangeBlindFilters.push('isActive');
        log.warning(
            'watchChanges cannot see the active -> inactive/awarded transition: activeOnly defaults to true, which '
            + 'sends SAM.gov the server-side filter is_active=true, and isActive is also the field this run watches '
            + 'most closely for changes. The moment a row flips inactive it stops matching the query entirely, so '
            + 'the change is never reported -- the run just says nothing was new. This fires on the DEFAULT '
            + 'setting, not just an opt-in filter.',
        );
    }
    if (!isWd && !isCfda && !isExclusions && noticeTypes.length) {
        watchChangeBlindFilters.push('noticeTypeCode');
        log.warning(
            'watchChanges cannot see the notice-type lifecycle change you are filtering on: noticeTypes is sent to '
            + 'SAM.gov as notice_type, and noticeTypeCode is also watched for changes. An opportunity whose notice '
            + 'type moves out of your filter (e.g. Solicitation -> Award) stops matching the query entirely, so '
            + 'that transition is never reported.',
        );
    }
    // A third instance, same class as the two above but on the Actor's OWN post-fetch filter
    // rather than a server-side one (cycle 2392): `responseDate` is a watched field, and
    // `deadlineFrom`/`deadlineTo` drop rows on exactly that value. A deadline extension that
    // pushes a row past `deadlineTo` -- the single highest-frequency real change in this niche per
    // the comment above snapshotOf -- removes the row from the result set, so changesBetween() is
    // never reached and the extension is never reported. Being client-side makes it no less blind.
    if (deadlineWindowSupported && (deadlineFrom || deadlineTo)) {
        watchChangeBlindFilters.push('responseDate');
        log.warning(
            'watchChanges cannot reliably see the deadline extension you are filtering on: '
            + `deadlineFrom/deadlineTo drop rows whose responseDate falls outside ${deadlineFrom ?? 'any'}..`
            + `${deadlineTo ?? 'any'}, and responseDate is also the field this run watches for changes. An `
            + 'agency extending a deadline past your window removes that row from the results, so the extension '
            + 'is never reported -- and a deadline moving INTO your window arrives as a brand-new row instead '
            + 'of a change.',
        );
    }
    if (watchChangeBlindFilters.length) {
        log.warning(
            'What to do: for isActive, pass activeOnly:false on the watch run (you get both active and inactive '
            + 'rows back, and can filter on isActive yourself after delivery) or run two labels -- one '
            + 'activeOnly:true for new rows, one activeOnly:false with watchChanges for the inactive transition. '
            + 'For noticeTypeCode, drop noticeTypes from the watch run and filter on noticeTypeCode yourself, or '
            + 'keep a separate unfiltered watchChanges label for lifecycle transitions.'
            + (watchChangeBlindFilters.includes('responseDate')
                ? ' For responseDate, drop deadlineFrom/deadlineTo from the watchChanges run (a one-sided '
                  + 'postedFrom window is change-blind to nothing, since publishDate never moves) and compare '
                  + 'each row\'s responseDate yourself after delivery.'
                : ''),
        );
    }
}

let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
const watchSeen = new Map(); // opportunityId -> last-seen snapshot
let changedCount = 0;
let skippedSeen = 0;

let baselineTruncated = 0; // ids dropped by WATCH_KEEP -- they come back as "new" and get charged

async function saveWatchRecord(status) {
    const all = Array.from(watchSeen.entries());
    const entries = all.slice(-WATCH_KEEP);
    baselineTruncated = all.length - entries.length;
    if (baselineTruncated > 0) {
        log.warning(
            `The baseline for "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the ${baselineTruncated} `
            + `oldest ${ROW_NOUN} id(s) were dropped and will be returned and CHARGED as new on a future run. `
            // dataType-aware: naicsCodes/setAsideTypes/noticeTypes are ignored (with their own warning)
            // for wd/cfda/exclusions, so telling those buyers to narrow by them would be advice that
            // provably does nothing -- same fix shape as the SEED_CAP note ~350 lines below.
            + `Narrow the watch query (a keyword${isWd ? ', a state' : (isCfda || isExclusions) ? ', an organization' : ', a NAICS code, a set-aside/notice type'}) or split it across labels.`,
        );
    }
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
        criteria: watchCriteria,
        lastRunAt: new Date().toISOString(),
        lastRunStatus: status,
        seenCount: entries.length,
        // Compact per-entry shape so WATCH_KEEP's 60,000 entries stay inside the KV record's size
        // budget: i(d), a(isActive), n(noticeTypeCode), r(responseDate), m(modifiedDate),
        // c(modificationsCount), w(awardeeName), h(descHash), v(revisionNumber), f(isFunded),
        // x(historicalIndexCount), t(terminationDate).
        seenIds: entries.map(([id, snap]) => ({
            i: id, a: snap.isActive, n: snap.noticeTypeCode, r: snap.responseDate, m: snap.modifiedDate,
            c: snap.modificationsCount, w: snap.awardeeName, h: snap.descHash, v: snap.revisionNumber,
            f: snap.isFunded, x: snap.historicalIndexCount, t: snap.terminationDate,
        })),
        runCount: (watchRecord.runCount ?? 0) + 1,
    });
}

if (watchMode) {
    watchStore = await Actor.openKeyValueStore(WATCH_STORE);
    const { key, fingerprint } = watchKeyFor(watchLabel, watchCriteria);
    watchKey = key;
    const existing = await watchStore.getValue(key);
    if (existing && Array.isArray(existing.seenIds)) {
        watchRecord = existing;
        // Backward-compatible reader: a record from before this feature existed would only ever
        // be a fresh baseline (this is the Actor's first watch-mode build), but kept defensive the
        // same way the fleet's other watch actors are, in case a future field is added later and
        // an older record is missing it -- missing fields just have no snapshot yet.
        for (const entry of existing.seenIds) {
            if (entry && typeof entry === 'object') {
                watchSeen.set(String(entry.i), {
                    isActive: entry.a ?? null, noticeTypeCode: entry.n ?? null, responseDate: entry.r ?? null,
                    modifiedDate: entry.m ?? null,
                    modificationsCount: typeof entry.c === 'number' ? entry.c : null,
                    awardeeName: entry.w ?? null, descHash: entry.h ?? null,
                    revisionNumber: typeof entry.v === 'number' ? entry.v : null,
                    isFunded: typeof entry.f === 'boolean' ? entry.f : null,
                    historicalIndexCount: typeof entry.x === 'number' ? entry.x : null,
                    terminationDate: entry.t ?? null,
                });
            } else {
                watchSeen.set(String(entry), {
                    isActive: null, noticeTypeCode: null, responseDate: null, modifiedDate: null,
                    modificationsCount: null, awardeeName: null, descHash: null, revisionNumber: null,
                    isFunded: null, historicalIndexCount: null, terminationDate: null,
                });
            }
        }
        log.info(
            `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
            + `${watchSeen.size} already-delivered ${ROW_NOUN}(s). Only ${ROW_NOUN_PLURAL} NOT in that baseline are returned and charged`
            + (watchChanges ? `, plus any already-delivered ${ROW_NOUN} whose ${WATCHED_FIELDS_TEXT} changed.` : '.'),
        );
    } else {
        watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
        seeding = true;
        log.info(
            `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
            + `It records which ${ROW_NOUN_PLURAL} already match and returns ZERO results (you are charged nothing). Run it `
            + 'again on the same label and filters -- on a schedule, typically -- to get only what is new since now.',
        );
    }
}

// This Actor is published PAY_PER_EVENT ($0.0015/row, single "result" event, see meta.json) but
// until this fix it only ever called Actor.pushData(results) in one bulk call at the end -- never
// Actor.charge(). Every other PPE Actor in the fleet routes pushes through a pushResult() that
// calls Actor.charge() first (federal-register-scraper/grants-gov-scraper/etc. all use this exact
// pattern); this one was published (cycle 540) without it, so every real buyer since would have
// gotten every row for free. Found and fixed cycle 542, before any paying run occurred (0 revenue
// booked fleet-wide as of this cycle, so no refund owed). `isPPE` guards local/non-PPE test runs,
// same as the sibling Actors.
let pushed = 0;
let chargeLimitReached = false;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item) {
    if (isPPE) {
        const r = await Actor.charge({ eventName: 'result', count: 1 });
        if (r.chargedCount === 0) { chargeLimitReached = true; return false; }
        await Actor.pushData(item); pushed += 1;
        if (r.eventChargeLimitReached) chargeLimitReached = true;
        return !r.eventChargeLimitReached && pushed < maxResults;
    }
    await Actor.pushData(item); pushed += 1;
    return pushed < maxResults;
}

const PAGE_SIZE = 100;

// Pulled out so the real run and a watch-mode baseline seed walk share the exact same paging
// logic and can never drift out of sync -- only the `limit` differs (maxResults vs. SEED_CAP).
const DEPTH_CAP = 10000; // SAM.gov's own hard backend paging depth, confirmed cycle 538

// How many of the declared matches this backend will actually hand over. null while SAM has not
// answered with a count -- never collapsed to 0, which is what made a failed count read as
// "nothing matched your filters" everywhere it was used.
function reachable() {
    return declaredMatches === null ? null : Math.min(declaredMatches, DEPTH_CAP);
}

async function fetchRows(limit) {
    // Before spending a single billable page: confirm SAM.gov still honours every filter name we
    // are about to send (see `assertFilterNamesApplied` above -- a dropped name fails OPEN).
    await assertFilterNamesApplied();
    const rows = [];
    // Measured live cycle 649 on a 19,834-match query: a full 100-page walk read 10,000 rows but
    // only 8,990 DISTINCT opportunity ids -- ~10% of rows repeat across pages, because SAM.gov
    // pages by offset over a live, relevance-sorted index that shifts under the walk. Every repeat
    // used to be pushed AND CHARGED again as a separate result. Dedupe inside the walk.
    const seenIds = new Set();
    const seenContentHashes = new Set(); // same-source republication guard; opportunities shape only
    let page = 0;
    while (rows.length < limit) {
        const reach = reachable();
        if (reach !== null && rows.length >= reach) break; // delivered everything SAM will serve
        if (!timeBudgetOk()) { markIncomplete('time-budget', timeBudgetDetail(rows.length)); break; }
        const url = buildSearchUrl(page, PAGE_SIZE);
        const data = await apiGet(url);
        if (!data) {
            // A null from apiGet has two causes and they need different names: SAM.gov genuinely
            // failing (`upstream-error` -- re-run once it recovers), and our own deadline guard
            // declining to start another request (`time-budget` -- nothing needs to recover, the
            // query is too big for this run's timeout). Reporting the second as an upstream error
            // would hand the buyer advice that provably does nothing, and would also feed the
            // seed-baseline guard below under the wrong label.
            if (timeBudgetExceeded) {
                markIncomplete('time-budget', timeBudgetDetail(rows.length));
                break;
            }
            pagesFailed += 1;
            markIncomplete('upstream-error', `page ${page} failed after 4 attempts (${lastApiError ?? 'unknown error'})`);
            log.warning(`Page ${page} failed after retries; stopping short.`);
            break;
        }
        pages += 1;
        // A 200 whose body carries no usable total is NOT "0 matches" -- the walk keeps paging blind
        // until SAM returns an empty page, instead of ending on the first page looking complete.
        const declared = Number.isFinite(data.page?.totalElements) ? Number(data.page.totalElements) : null;
        // FIRST answer wins. Measured live cycle 649: walking a 911-match query to exhaustion, the
        // one-past-the-end page comes back 200 with an empty `results` AND `totalElements: 0`, so
        // re-assigning on every page clobbered the real count with 0 on the very last read --
        // RUN_SUMMARY would have published `declaredMatches: 0` for a 911-match query and the
        // duplicate/short-page checks (`rows.length < 0`) could never fire. The declared count is a
        // property of the query, measured once, not a per-page field.
        if (declared !== null && declaredMatches === null) declaredMatches = declared;
        const pageRows = data._embedded?.results ?? [];
        if (pageRows.length === 0) {
            // Empty page before SAM's own declared total is reached = the backend quit early, which
            // is not the same fact as "the result set ended here".
            const reachNow = reachable();
            if (reachNow !== null && rows.length < reachNow) {
                // Distinguish "SAM.gov quit early" from "SAM.gov served its whole set but repeated
                // rows, so there were fewer distinct opportunities than it declared". Both come up
                // short of the declared total; only the first is an upstream failure.
                // A date window (cycle 2392) makes `rows.length < declared` the NORMAL outcome, not
                // a shortfall: SAM.gov's declared total counts everything matching the SERVER-side
                // filters, and the window is applied after the fetch. Reconcile the window drops
                // before calling an exhausted walk incomplete -- without this, every single
                // windowed run would finish with a false `short-page` incompleteness and a scary
                // Console status for working exactly as designed.
                const clientDropped = postFetchFilterDroppedCount();
                if (clientDropped > 0 && rows.length + duplicateRowsDropped + clientDropped >= reachNow) {
                    log.info(
                        `Walk complete: SAM.gov served all ${reachNow} row(s) it declared for these filters; `
                        + `${clientDropped} were dropped by ${postFetchFilterText()}`
                        + `${duplicateRowsDropped ? ` and ${duplicateRowsDropped} were repeats` : ''}, leaving `
                        + `${rows.length} ${ROW_NOUN_PLURAL}. Nothing is missing -- this run is COMPLETE.`,
                    );
                } else if (rows.length + duplicateRowsDropped >= reachNow) {
                    markIncomplete('duplicate-rows', `SAM.gov served ${reachNow} row(s) for this query but only ${rows.length} were distinct opportunities (${duplicateRowsDropped} repeat(s) dropped, uncharged)`);
                } else {
                    markIncomplete('short-page', `SAM.gov returned an empty page ${page} after ${rows.length} of ${reachNow} reachable match(es)`
                        + (clientDropped > 0 ? `, plus ${clientDropped} dropped by ${postFetchFilterText()} -- the shortfall is bigger than that explains` : ''));
                }
            }
            break;
        }
        scanned += pageRows.length;
        for (const row of pageRows) {
            if (isExclusions && row.noPublicDisplayFlag === 'T') { noPublicDisplaySuppressed += 1; continue; }
            const item = isWd ? normalizeWdRow(row) : isCfda ? normalizeCfdaRow(row) : isExclusions ? normalizeExclusionRow(row) : normalizeRow(row);
            // The posted/deadline window (cycle 2392), applied here -- inside the walk, before the
            // row is collected -- so an out-of-window row is never pushed and never charged, and
            // does not consume one of the buyer's `maxResults` slots. Ordered BEFORE the dedupe
            // guards on purpose: it keeps each counter unambiguous (`dateWindowDropped` = outside
            // your window, `duplicateRowsDropped` = a repeat among the rows that were inside it),
            // which is what the empty-page reconciliation below reads to tell a windowed run from
            // a genuinely short one.
            if (!inDateWindow(item)) continue;
            // Same pre-dedupe placement and reasoning as inDateWindow() above: a solicitation
            // number lookup is also a pre-charge filter, and ordering it before the dedupe guards
            // keeps duplicateRowsDropped meaning strictly "a repeat among rows that matched".
            if (!matchesSolicitationNumber(item)) continue;
            // Same pre-dedupe placement and reasoning as the two filters above.
            if (!inAwardAmountRange(item)) continue;
            const rowId = idOf(item);
            if (rowId) {
                if (seenIds.has(rowId)) { duplicateRowsDropped += 1; continue; }
                seenIds.add(rowId);
            }
            if (!isWd && !isCfda && !isExclusions) {
                const contentHash = [item.solicitationNumber, item.noticeTypeCode, item.title, descHashOf(item.description)].join('|');
                if (seenContentHashes.has(contentHash)) { republishedRowsDropped += 1; continue; }
                seenContentHashes.add(contentHash);
            }
            rows.push(item);
            if (rows.length >= limit) break;
        }
        const target = reachable() === null ? limit : Math.min(reachable(), limit);
        log.info(`Page ${page}: +${pageRows.length} rows (total so far ${rows.length}/${target})`);
        page += 1;
        if (page * PAGE_SIZE >= DEPTH_CAP) {
            // Only a shortfall if there was actually more to get and the caller still wanted it.
            if (rows.length < limit && (declaredMatches === null || declaredMatches > DEPTH_CAP)) {
                markIncomplete(
                    'depth-cap',
                    `SAM.gov serves at most ${DEPTH_CAP} rows per query`
                    + `${declaredMatches === null ? '' : `; ${declaredMatches - DEPTH_CAP} of ${declaredMatches} match(es) sit past it`}`,
                );
            }
            log.warning('Hit SAM.gov\'s 10,000-row backend depth cap; narrow keyword/filters for more.');
            break;
        }
        await sleep(300); // stay well under any rate limit; verified spacing from the feasibility check
    }
    return rows;
}

// Seeding only needs ids + the watched fields, both already on the thin search row, so it never
// needs enrichDetail on -- unlike grants-gov-scraper's award-amount filter, nothing this Actor
// watches lives only on the detail record. It walks the WHOLE match set (up to SEED_CAP, the same
// as SAM.gov's own hard depth cap), unbounded by maxResults -- a baseline that stopped early would
// report every opportunity past the stopping point as "new" on the first incremental run.
if (watchMode && seeding) {
    const baselineRows = await fetchRows(SEED_CAP);
    for (const row of baselineRows) {
        if (idOf(row)) watchSeen.set(idOf(row), snapshotOf(row));
    }
    // Backstop, keyed on rows READ not rows kept: if the seed asks for exactly SEED_CAP distinct
    // rows and SAM.gov happens to serve no duplicates, the walk exits on `rows.length >= limit`
    // before fetchRows' own depth-cap branch is reached. A baseline that stopped at the cap is the
    // same over-charge as one that stopped on an error, so it is marked either way. Same
    // `depth-cap` reason on purpose -- one name per fact; `mode: "watch-seed"` says it was a seed.
    if (scanned >= SEED_CAP && (declaredMatches === null || declaredMatches > SEED_CAP)) {
        markIncomplete(
            'depth-cap',
            `the baseline walk stopped at SAM.gov's ${SEED_CAP}-row depth cap`
            + `${declaredMatches === null ? '' : `; ${(declaredMatches - SEED_CAP).toLocaleString('en-US')} of ${declaredMatches.toLocaleString('en-US')} match(es) were never seen`}`,
        );
    }
    log.info(`Baseline walk: ${watchSeen.size} ${ROW_NOUN} id(s) recorded.`);
}

let results = [];
let rowsNotReached = 0; // fetched rows the push loop never got to (charge limit / maxResults)
if (!seeding) {
    results = await fetchRows(maxResults);
    // The walk delivered all it was asked for, but SAM says there is more behind it. That is a
    // legitimate, buyer-chosen shortfall -- it still has to be SAID, because a pipeline cannot tell
    // "200 of 200 matches" from "200 of 12,297" by looking at the dataset.
    const reach = reachable();
    if (results.length >= maxResults && reach !== null && reach > maxResults) {
        markIncomplete('max-results', `maxResults=${maxResults} of ${reach} reachable match(es)`);
    }
    if (enrichDetail) log.info(`Enriching up to ${results.length} row(s) with detail-call fields (naics, set-aside, place of performance, contacts) as each is reached...`);
    if (includeAttachments) log.info(`Fetching attachment lists for up to ${results.length} row(s) as each is reached...`);

    let beforePush = 0;
    let index = 0;
    for (const item of results) {
        // Gated ONLY when there is per-row network work. With enrichDetail and includeAttachments
        // both off this loop is pure pushData -- no HTTP, no sleep -- so stopping it on the clock
        // would abandon already-fetched rows to buy back milliseconds; the 45s margin exists to
        // flush exactly those. With either on, every row costs 1-2 HTTP calls plus 200-400ms, so
        // the loop genuinely can run into the deadline. Then stopping is the honest move: the
        // alternative is delivering (and CHARGING for) rows whose paid-for detail/attachment
        // fields are null for a reason that has nothing to do with SAM.gov.
        if ((enrichDetail || includeAttachments) && !timeBudgetOk()) {
            rowsNotReached = results.length - index;
            log.warning(`Run time budget reached after ${index} enriched row(s); ${rowsNotReached} fetched row(s) not delivered.`);
            break;
        }
        index += 1;
        // Enrich/fetch-attachments immediately before this row is decided on, one row at a time,
        // instead of two separate full passes over `results` before any row is pushed. Under the
        // old order a platform hard kill mid-run lost 100% of the rows (and wrote no RUN_SUMMARY)
        // even though some had already been fully enriched -- enrichment never bought any row
        // safety because nothing was pushed/charged until every row had been enriched first. Now a
        // hard kill loses only the not-yet-reached tail, same as a run with enrichment off.
        if (enrichDetail) { await enrichOne(item); await sleep(200); }
        if (includeAttachments) { await fetchAttachments(item); await sleep(200); }
        if (watchMode && idOf(item) && watchSeen.has(idOf(item))) {
            const id = idOf(item);
            const nextSnap = snapshotOf(item);
            // Already delivered under this watch label. Normally dropped before any charge, so an
            // opportunity is never paid for twice -- UNLESS watchChanges is on and one of the
            // watched fields moved since we last saw it, in which case it's re-delivered (charged
            // like a new row) tagged with exactly what changed.
            const change = watchChanges ? changesBetween(watchSeen.get(id), nextSnap) : null;
            if (!change) {
                // Snapshot is kept current either way, so turning watchChanges on later detects
                // only drift from that point, not a backlog since the baseline.
                watchSeen.set(id, nextSnap);
                skippedSeen += 1;
                continue;
            }
            const cont = await pushResult({ ...item, _watchChangeType: change.types, _watchPrevious: change.previous });
            if (pushed > beforePush) { watchSeen.set(id, nextSnap); changedCount += 1; }
            beforePush = pushed;
            if (!cont) { rowsNotReached = results.length - index; break; }
            continue;
        }
        const cont = await pushResult(item);
        // Recorded as delivered only after the charge actually succeeded -- anything dropped by
        // maxResults or a charge limit stays "new" for the next run.
        if (watchMode && idOf(item) && pushed > beforePush) watchSeen.set(idOf(item), snapshotOf(item));
        beforePush = pushed;
        if (!cont) { rowsNotReached = results.length - index; break; } // maxResults reached or a per-run charge limit hit
    }

    // Same first-cause-wins priority as before the enrichment reorder, just evaluated after the
    // loop now that enrichment happens row-by-row inside it rather than in a pass that finished
    // before the loop started: enrich-failed, then attachments-failed, then charge-limit/
    // max-results. `index` (rows actually reached before an early break), not `results.length`, is
    // the right denominator -- a maxResults/charge-limit break can leave both failure counts well
    // under `results.length` while still being 100% of what was attempted.
    // A detail call that failed leaves naicsCodes/setAside/pointOfContact at null -- the same
    // null a genuinely contact-less notice has. The buyer turned enrichment ON and paid for
    // those fields, so a silent miss is a shortfall, not a detail.
    // Ahead of enrich-failed/charge-limit/max-results on purpose. If the clock ran out while the
    // LAST row was being enriched the loop ends naturally with no break, so nothing inside it
    // marked the cause -- and the detail call that the guard aborted would otherwise be reported
    // as `enrich-failed`, blaming SAM.gov for our own deadline. First-cause-wins makes this a
    // no-op when the walk or the loop already named it.
    if (timeBudgetExceeded) markIncomplete('time-budget', timeBudgetDetail(pushed));
    if (enrichDetail && detailLookupsFailed) {
        markIncomplete('enrich-failed', `${detailLookupsFailed} of ${index} detail lookup(s) failed; their naics/set-aside/place-of-performance/contact fields are null for that reason, not because SAM.gov has none`);
    }
    // Same null-means-broken rule as enrich-failed above: an attachments lookup that failed
    // leaves `attachments: null`, not `[]` (a notice with genuinely zero files is `[]`).
    if (includeAttachments && attachmentLookupsFailed) {
        markIncomplete('attachments-failed', `${attachmentLookupsFailed} of ${index} attachment lookup(s) failed; their attachments field is null for that reason, not because the notice has none`);
    }

    // The push loop abandoning rows it had already fetched is invisible in the dataset: the run
    // SUCCEEDS with a plausible-looking row count. Charge limit is reported ahead of maxResults --
    // it is the cause the buyer did not choose.
    if (chargeLimitReached) {
        markIncomplete('charge-limit', `the run's pay-per-event charge limit was reached${rowsNotReached ? `; ${rowsNotReached} already-fetched row(s) were not delivered` : ''}`);
    } else if (rowsNotReached > 0) {
        markIncomplete('max-results', `maxResults=${maxResults} reached; ${rowsNotReached} already-fetched row(s) were not delivered`);
    }
}

// A SEED walk cut short by SAM.gov not answering (`upstream-error`) or quitting early before its
// own declared total, unexplained by duplicates (`short-page`), is not a smaller baseline, it is a
// WRONG one: every opportunity past the failure point would read as "new" (and charged) on the
// first incremental run. `depth-cap` and `duplicate-rows` are deliberately excluded -- both mean
// SAM.gov answered IN FULL (its own hard 10,000-row limit, or repeats within what it did serve),
// so a capped-but-real baseline is still strictly better than none. Seeding never charges, so
// refusing to save costs nothing but a re-run. Before this fix the save was unconditional and only
// the status label read `'seeded-incomplete'` -- cosmetic, since neither load path (line ~751)
// reads `.status` back, so the truncated baseline was consumed exactly like a complete one.
// `time-budget` belongs in this set for exactly the same reason as the two upstream causes, which
// is why the set is no longer named after them: a baseline cut short by OUR OWN clock is just as
// wrong as one cut short by SAM.gov -- every opportunity past the stopping point still reads as
// "new" (and billable) on the first incremental run. What differs is only the advice below.
const SEED_FATAL_SHORTFALLS = new Set(['upstream-error', 'short-page', 'time-budget']);
const seedFailure = seeding && incompleteReason && SEED_FATAL_SHORTFALLS.has(incompleteReason)
    ? `${incompleteReason}${incompleteDetail ? `: ${incompleteDetail}` : ''}`
    : null;
// Third branch, not a safe default: "once SAM.gov is answering" is right for an upstream stop and
// actively wrong for a clock stop (nothing needs to recover; an identical re-run stops identically).
const seedRetryAdvice = incompleteReason === 'time-budget'
    ? 'Re-run with the same watchLabel once the query is narrower or the run has a longer timeout'
    : 'Re-run with the same watchLabel to seed again once SAM.gov is answering';

if (watchMode && seedFailure) {
    log.warning(
        `Baseline walk for watch label "${watchLabel}" was cut short (${seedFailure}), so NO baseline was saved. `
        + `${seedRetryAdvice} -- saving a truncated baseline `
        + 'would make every opportunity past the failure point look "new" (and billable) on the first incremental run.',
    );
} else if (watchMode) {
    await saveWatchRecord(
        seeding
            ? (complete ? 'seeded' : 'seeded-incomplete')
            : (complete ? 'incremental' : 'incremental-incomplete'),
    );
    if (seeding) {
        // An incomplete-but-saved baseline here means depth-cap/duplicate-rows only -- SAM.gov
        // answered in full, so this is a real (if capped) baseline, not the over-charge risk above.
        if (!complete) {
            log.warning(
                `BASELINE INCOMPLETE (${incompleteReason}${incompleteDetail ? `: ${incompleteDetail}` : ''}). Only `
                + `${watchSeen.size} ${ROW_NOUN}(s) were recorded as already-seen out of `
                + `${declaredMatches === null ? 'an unknown number of' : declaredMatches.toLocaleString('en-US')} match(es). `
                + `Re-run this seed before scheduling incremental runs, or the missing ${ROW_NOUN_PLURAL} will be returned and CHARGED as new.`,
            );
        }
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} ${ROW_NOUN}(s) recorded as already-seen, `
            + `0 results returned, 0 charged. The next run on this label and these filters returns only new ${ROW_NOUN_PLURAL}.`
            + (watchSeen.size >= SEED_CAP
                ? ` NOTE: the baseline stopped at the ${SEED_CAP}-record cap. Narrow the query (a keyword`
                + `${isCfda || isExclusions ? ', an organization' : isWd ? ', a state' : ', a NAICS code, a set-aside/notice type'}) so `
                + `the whole result set fits, or the first incremental run will report ${ROW_NOUN_PLURAL} past the cap as new.`
                : ''),
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed - changedCount} new ${ROW_NOUN}(s)`
            + (watchChanges ? ` and ${changedCount} changed ${ROW_NOUN}(s) (${WATCHED_FIELDS_TEXT})` : '')
            + ` since the last run (${skippedSeen} already-delivered, unchanged row(s) skipped, uncharged); baseline now holds ${watchSeen.size}.`
            // Without this, a run that CAN NEVER report one of its blind fields changing (see the
            // watchChangeBlindFilters warnings above) is byte-for-byte indistinguishable from a
            // healthy quiet run -- and this is a monitor, so the buyer schedules it and stops looking.
            + (pushed === 0 && watchChangeBlindFilters.length
                ? ` NOTE: this run also cannot report any ${watchChangeBlindFilters.join('/')} change at all (see `
                + 'the change-blind-filter warning(s) above), so "nothing changed" is not evidence here.'
                : ''),
        );
    }
}

log.info(`Done. Pushed ${pushed} ${ROW_NOUN_PLURAL} (scanned ${scanned} row(s) over ${pages} page(s)).`
    + (isExclusions ? ` ${noPublicDisplaySuppressed} row(s) suppressed by SAM.gov's own do-not-display flag.` : '')
    + ((!isWd && !isCfda && !isExclusions && republishedRowsDropped > 0) ? ` ${republishedRowsDropped} republished duplicate row(s) dropped, uncharged.` : '')
    + (dateWindowActive
        ? ` Date window (${dateWindowText()}): ${dateWindowDropped} row(s) dropped outside it`
          + `${dateWindowMissing > 0 ? ` and ${dateWindowMissing} with no readable date` : ''}, uncharged.`
        : '')
    + (solicitationNumberActive
        ? ` solicitationNumber "${solicitationNumberRaw}": ${solicitationNumberMismatch} non-matching row(s) dropped`
          + `${solicitationNumberMissing > 0 ? ` and ${solicitationNumberMissing} with no solicitation number` : ''}, uncharged.`
        : '')
    + (awardAmountActive
        ? ` ${awardAmountText()}: ${awardAmountDropped} out-of-range row(s) dropped`
          + `${awardAmountMissing > 0 ? ` and ${awardAmountMissing} with no award amount` : ''}, uncharged.`
        : ''));

// ---------------------------------------------------------------------------
// RUN_SUMMARY: this run's completeness, in a form a pipeline can read. Fetch with
//   GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
// which needs no webhook. `complete` is deliberately kept OUT of the status string: a run can be
// SUCCEEDED and short at the same time, and that pair is exactly what this record exists for.
const runSummary = {
    dataType,
    searchIndex: SEARCH_INDEX,
    mode: watchMode ? (seeding ? 'watch-seed' : 'watch-incremental') : 'search',
    // What SAM.gov itself says matches this query (page.totalElements). `null` means the search
    // never answered with a count -- never read it as 0.
    declaredMatches,
    // Of those, how many this backend will actually serve, given its 10,000-row depth cap.
    reachableMatches: reachable(),
    unreachableMatches: declaredMatches === null ? null : Math.max(declaredMatches - DEPTH_CAP, 0),
    depthCap: DEPTH_CAP,
    scanned,
    delivered: pushed,
    rowsNotReached,
    pages,
    pagesFailed,
    // Distinct is what you are charged for: `scanned` counts raw rows off the wire,
    // `scanned - duplicateRowsDropped` is how many distinct opportunities that actually was.
    duplicateRowsDropped,
    republishedRowsDropped: (!isWd && !isCfda && !isExclusions) ? republishedRowsDropped : null,
    noPublicDisplaySuppressed: isExclusions ? noPublicDisplaySuppressed : null,
    complete,
    incompleteReason,
    incompleteDetail,
    // Which filter(s) lost blank entries before the query was built, and how many each lost
    // (cycle 2356). Null, not {}, when nothing was dropped, so a consumer can tell "this field
    // existed and was empty" from "this build does not report it".
    blankFilterEntriesDropped: Object.keys(blankFilterEntriesDropped).length ? blankFilterEntriesDropped : null,
    // The posted/deadline window this run applied, and what it cost you nothing to drop (cycle
    // 2392). `declaredMatches` above is SAM.gov's PRE-window count -- these three fields are what
    // reconcile it with `delivered`, and a consumer should not read `delivered < declaredMatches`
    // as a shortfall without subtracting them first. Null, not 0/{}, when no window was set.
    dateWindow: dateWindowActive ? { postedFrom, postedTo, deadlineFrom, deadlineTo } : null,
    dateWindowDropped: dateWindowActive ? dateWindowDropped : null,
    dateWindowMissing: dateWindowActive ? dateWindowMissing : null,
    // Same reconciliation role as the date-window fields above, for the solicitation-number
    // exact-match filter (cycle 2395): null, not 0, when no value was given.
    solicitationNumber: solicitationNumberActive ? solicitationNumberClean : null,
    solicitationNumberMismatch: solicitationNumberActive ? solicitationNumberMismatch : null,
    solicitationNumberMissing: solicitationNumberActive ? solicitationNumberMissing : null,
    // Whether the cycle-2397 notice_id fast path found this run's raw value server-side (one
    // request, no full-text walk) versus falling back to the q=<clean> walk. Null, not false,
    // when solicitationNumber was not set at all.
    noticeIdFastPath: solicitationNumberActive ? noticeIdFastPathActive : null,
    // Same reconciliation role as the two filters above, for the award-amount range (cycle 2398):
    // null, not 0, when neither minAwardAmount nor maxAwardAmount was given.
    awardAmountRange: awardAmountActive ? { minAwardAmount, maxAwardAmount } : null,
    awardAmountDropped: awardAmountActive ? awardAmountDropped : null,
    awardAmountMissing: awardAmountActive ? awardAmountMissing : null,
    lastApiError,
    maxResults,
    chargeLimitReached,
    detailLookupsFailed: enrichDetail ? detailLookupsFailed : null,
    attachmentLookupsFailed: includeAttachments ? attachmentLookupsFailed : null,
    watchLabel: watchMode ? watchLabel : null,
    watchSeeding: watchMode ? seeding : null,
    baselineSize: watchMode ? watchSeen.size : null,
    baselineTruncated: watchMode ? baselineTruncated : null,
    changedRedelivered: watchMode && !seeding ? changedCount : null,
    skippedSeen: watchMode && !seeding ? skippedSeen : null,
    watchChangeBlindFilters: watchMode && watchChanges ? watchChangeBlindFilters : null,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

// A short run still SUCCEEDS (the rows it did get are real and already charged), so the status
// message is the only place the Apify console itself shows the shortfall. There was no
// setStatusMessage call anywhere in this Actor before cycle 649.
if (!complete) {
    const of = reachable() === null ? '' : ` of ${reachable().toLocaleString('en-US')} reachable`;
    await Actor.setStatusMessage(
        seeding
            ? `Baseline INCOMPLETE: ${watchSeen.size.toLocaleString('en-US')} ${ROW_NOUN}(s) recorded${of} — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. Re-seed before scheduling, or the rest will be charged as new. See RUN_SUMMARY.`
              + blankDropNote()
            : `Incomplete: ${pushed.toLocaleString('en-US')} row(s)${of} — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. See RUN_SUMMARY for details.`
              + blankDropNote(),
    );
} else if (watchMode && !seeding && pushed === 0 && skippedSeen > 0) {
    // Every row this query matched was already delivered under this watch label and none changed
    // -- the common, expected result on a scheduled re-run, not a failure. Before this branch
    // existed the only trace was a log.info line (above, in the push loop); the Console showed a
    // green run next to an empty dataset with nothing to tell a buyer who only reads run status.
    // Seeding is excluded -- 0 rows on a baseline run is the DESIGNED result (see the
    // baseline-saved log line emitted during the walk), not a quiet incremental run.
    await Actor.setStatusMessage(
        `Nothing new for watch label "${watchLabel}": all ${skippedSeen.toLocaleString('en-US')} matching ${ROW_NOUN}(s) `
        + `were already delivered on a prior run${watchChanges ? ' and none of their watched fields changed' : ''}. `
        + `You were charged nothing.${watchChanges ? '' : ' Set watchChanges: true to also catch edits to already-delivered rows.'}`
        + blankDropNote(),
    );
} else if (!seeding && pushed === 0) {
    // The other way this Actor can reach SUCCEEDED with 0 rows and no markIncomplete cause above:
    // every filter value supplied is valid and SAM.gov simply has no match -- covers a plain search
    // AND a watch run whose underlying query now matches nothing at all (the skippedSeen>0 branch
    // above only fires once there is something to compare against). Only name filters that differ
    // from this dataType's default AND actually apply to it -- naicsCodes/setAsideTypes/noticeTypes
    // are opportunities-only, states is ignored on cfda/exclusions, organizationId is ignored on wd
    // (see the per-dataType ignore blocks above) -- naming a filter the buyer never supplied, or one
    // this dataType silently drops, would be the same wrong-knob mistake cycle 1637 already ruled
    // out elsewhere in this fleet.
    const appliedFilters = [];
    // keyword is never actually sent when solicitationNumber is active -- it takes over `q`
    // entirely in buildSearchUrl -- so naming it here would be the exact false-applied-filter
    // claim this block exists to avoid (cycle 1637).
    if (keyword && !solicitationNumberActive) appliedFilters.push(`keyword "${keyword}"`);
    if (!isWd && !isCfda && !isExclusions && naicsCodes.length) appliedFilters.push(`naicsCodes ${naicsCodes.join(', ')}`);
    if (!isWd && !isCfda && !isExclusions && setAsideTypes.length) appliedFilters.push(`setAsideTypes ${setAsideTypes.join(', ')}`);
    if (!isWd && !isCfda && !isExclusions && noticeTypes.length) appliedFilters.push(`noticeTypes ${noticeTypes.join(', ')}`);
    if (!isCfda && !isExclusions && states.length) appliedFilters.push(`states ${states.join(', ')}`);
    if (!isWd && organizationId) appliedFilters.push(`organizationId ${organizationId}`);
    // The date window is the one filter here that can be the sole reason for an empty run while
    // SAM.gov itself declared hundreds of matches, so it names its own drop count (cycle 2392).
    if (dateWindowActive) {
        appliedFilters.push(`your date window (${dateWindowText()}), which dropped `
            + `${dateWindowDropped + dateWindowMissing} fetched row(s)`);
    }
    if (solicitationNumberActive) {
        appliedFilters.push(`solicitationNumber "${solicitationNumberRaw}", which dropped `
            + `${solicitationNumberMismatch + solicitationNumberMissing} fetched row(s)`);
    }
    if (awardAmountActive) {
        appliedFilters.push(`your ${awardAmountText()} range, which dropped `
            + `${awardAmountDropped + awardAmountMissing} fetched row(s)`);
    }
    await Actor.setStatusMessage(
        appliedFilters.length
            ? `0 ${ROW_NOUN_PLURAL} matched: SAM.gov has none once ${appliedFilters.join(' + ')} ${appliedFilters.length > 1 ? 'are' : 'is'} applied. `
              + 'Every value you gave is valid, so this is a genuinely empty search, not an input mistake -- drop or widen one filter at a '
              + 'time to find which one excludes everything. You were charged nothing.'
              + blankDropNote()
            : `0 ${ROW_NOUN_PLURAL} matched: SAM.gov has no ${ROW_NOUN} at all for this query, with no filter narrowing the run. You were charged nothing.`
              + blankDropNote(),
    );
} else {
    if (declaredMatches !== null && !watchMode && !postFetchFilterActive) {
        log.info(`Complete: delivered every one of the ${declaredMatches.toLocaleString('en-US')} ${ROW_NOUN}(s) SAM.gov declared for these filters.`);
    } else if (declaredMatches !== null && !watchMode) {
        // Same line, but it must NOT claim to have delivered SAM's declared total when a date
        // window or solicitation-number lookup was applied after the fetch -- `declaredMatches` is
        // the pre-filter count (cycle 2392), so saying "delivered every one of the 340" next to 12
        // pushed rows would be the same false-claim class this Actor's README was corrected for in
        // cycle 2391.
        log.info(
            `Complete: of the ${declaredMatches.toLocaleString('en-US')} ${ROW_NOUN}(s) SAM.gov declared for these `
            + `filters, ${pushed.toLocaleString('en-US')} matched ${postFetchFilterText()} and were delivered; `
            + `${postFetchFilterDroppedCount().toLocaleString('en-US')} were read and dropped, uncharged.`,
        );
    }
    // A clean run that DELIVERED rows is the one path that previously set no status message at all
    // (cycle 2356) -- so a partial blank drop, which silently narrows the search the buyer asked
    // for, was invisible in the Console on exactly the runs that get charged. Only set a message
    // when there is actually something to say; a healthy unqualified run keeps Apify's default.
    const note = blankDropNote();
    // A windowed run also gets a message on the one path that otherwise sets none: the Console
    // shows `delivered` next to nothing explaining why it is so much smaller than SAM.gov's own
    // declared total, and the window is applied after the fetch so that gap is expected, not a
    // fault (cycle 2392).
    const windowNote = postFetchFilterActive
        ? ` ${postFetchFilterDroppedCount().toLocaleString('en-US')} fetched row(s) dropped by ${postFetchFilterText()} `
          + `before charging${declaredMatches !== null ? `, out of ${declaredMatches.toLocaleString('en-US')} SAM.gov declared for your other filters` : ''}.`
        : '';
    if (note || windowNote) {
        await Actor.setStatusMessage(
            `Delivered ${pushed.toLocaleString('en-US')} ${ROW_NOUN}(s).${windowNote}${note}`,
        );
    }
}

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill -- best-effort only, one attempt, short timeout, failures are
// a warning not a thrown error. `watchNewCount` is `pushed - changedCount` because this Actor
// pushes new AND changed rows through the same counter (cycle 441 lesson).
if (webhookUrl) {
    const env = Actor.getEnv();
    const payload = {
        actorRunId: env.actorRunId ?? null,
        defaultDatasetId: env.defaultDatasetId ?? null,
        finishedAt: new Date().toISOString(),
        pushed,
        rowsScanned: scanned, // raw rows read from SAM.gov, seed walk included -- `results.length`
        // was 0 on every baseline run no matter how many thousands it walked.
        watchLabel: watchMode ? watchLabel : null,
        watchSeeding: watchMode ? seeding : null,
        watchNewCount: watchMode && !seeding ? pushed - changedCount : null,
        watchChangedCount: watchMode && !seeding && watchChanges ? changedCount : null,
        watchSkippedCount: watchMode && !seeding ? skippedSeen : null,
        // Same object as the RUN_SUMMARY key-value record, so a webhook consumer and a
        // console/API consumer read the identical completeness facts.
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

if (watchMode && seedFailure) {
    await Actor.fail(
        `The watch baseline could not be completed: ${seedFailure.replace(/[.\s]*$/, '')}. No baseline was saved `
        + `for watch label "${watchLabel}" -- ${seedRetryAdvice.replace(/^Re-run/, 're-run')}.`,
    );
}

await Actor.exit();
