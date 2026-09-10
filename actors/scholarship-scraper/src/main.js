// scholarship-scraper — bold.org scholarship listings, HTTP-only (no headless browser, no proxy).
//
// How it works: bold.org is a Next.js App Router site. Every category page
// (/scholarships/by-major/<slug>/ etc.) ships the *full* scholarship records for that
// category inside the RSC flight payload in the initial HTML — ~30 complete records per
// single HTTP request, no JS execution needed. We reassemble the flight stream from the
// self.__next_f.push([1,"..."]) script chunks, then slice out the embedded JSON.
// robots.txt allows plain paths and only disallows query-string URLs (`Disallow: /*?*`),
// so we never request a URL with a query string.
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const BASE = 'https://bold.org';
const CATEGORY_TYPES = ['by-major', 'by-state', 'by-type', 'by-demographics', 'by-year'];

const maxResults = Math.min(Number(input.maxResults ?? 200), 10000);
const maxCategoryPages = Math.min(Number(input.maxCategoryPages ?? 20), 600);
const categoryTypes = (Array.isArray(input.categoryTypes) && input.categoryTypes.length
    ? input.categoryTypes
    : ['by-major']).filter((t) => CATEGORY_TYPES.includes(t));
const startUrls = (input.startUrls ?? []).map((u) => (typeof u === 'string' ? u : u?.url)).filter(Boolean);
const openOnly = input.openOnly !== false;
const includeEssayPrompt = input.includeEssayPrompt !== false;
const minAwardAmount = input.minAwardAmount == null ? null : Number(input.minAwardAmount);
const deadlineBefore = input.deadlineBefore ? Date.parse(input.deadlineBefore) : null;
const deadlineAfter = input.deadlineAfter ? Date.parse(input.deadlineAfter) : null;
const educationLevels = (input.educationLevels ?? []).map((s) => String(s).replace(/^_/, '').toLowerCase());
// Free-text search. "scholarship(s)" is dropped as a stopword so "nursing scholarships" behaves
// like "nursing"; every remaining token must appear somewhere in the record's text.
const searchTokens = String(input.searchQuery ?? '')
    .toLowerCase()
    .split(/[^a-z0-9+#]+/)
    .filter((t) => t && !/^scholarships?$/.test(t));

const cm = Actor.getChargingManager();
const isPPE = cm.getPricingInfo().isPayPerEvent;
let pushed = 0;

async function pushResult(item) {
    if (isPPE) {
        const r = await Actor.charge({ eventName: 'result', count: 1 });
        if (r.chargedCount === 0) return false; // user's budget exhausted: never push unpaid items
        await Actor.pushData(item);
        pushed += 1;
        return !r.eventChargeLimitReached && pushed < maxResults;
    }
    await Actor.pushData(item);
    pushed += 1;
    return pushed < maxResults;
}

async function fetchHtml(url) {
    const res = await gotScraping({
        url,
        timeout: { request: 45000 },
        retry: { limit: 2 },
        headers: { accept: 'text/html,application/xhtml+xml' },
        throwHttpErrors: false,
    });
    if (res.statusCode !== 200) {
        log.warning(`HTTP ${res.statusCode} for ${url} — skipped.`);
        return null;
    }
    return res.body;
}

// --- RSC flight payload helpers -------------------------------------------------

/** Reassemble the React flight stream that Next.js splits across __next_f.push() calls. */
function flightStream(html) {
    const re = /self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)/g;
    let m;
    let buf = '';
    while ((m = re.exec(html)) !== null) {
        try {
            buf += JSON.parse(m[1]);
        } catch {
            /* a chunk we cannot decode is not fatal; the payload we want may still be intact */
        }
    }
    return buf;
}

/** Return the JSON text of the array/object that starts at `start` (must point at '[' or '{'). */
function sliceJson(s, start) {
    const open = s[start];
    if (open !== '[' && open !== '{') return null;
    const close = open === '[' ? ']' : '}';
    let depth = 0;
    let inStr = false;
    let esc = false;
    for (let i = start; i < s.length; i++) {
        const c = s[i];
        if (inStr) {
            if (esc) esc = false;
            else if (c === '\\') esc = true;
            else if (c === '"') inStr = false;
            continue;
        }
        if (c === '"') inStr = true;
        else if (c === open) depth += 1;
        else if (c === close) {
            depth -= 1;
            if (depth === 0) return s.slice(start, i + 1);
        }
    }
    return null;
}

function extractAtKey(stream, key) {
    let from = 0;
    const out = [];
    for (;;) {
        const i = stream.indexOf(key, from);
        if (i === -1) return out;
        const txt = sliceJson(stream, i + key.length - 1);
        from = i + key.length;
        if (!txt) continue;
        try {
            out.push(JSON.parse(txt));
        } catch {
            /* not the blob we want */
        }
    }
}

/** All scholarship records embedded in one bold.org page (category page or detail page). */
function scholarshipsFromHtml(html) {
    const stream = flightStream(html);
    const found = [];
    for (const arr of extractAtKey(stream, '"scholarships":[')) {
        if (Array.isArray(arr)) found.push(...arr.filter((s) => s && s.slug && s.name));
    }
    if (!found.length) {
        for (const obj of extractAtKey(stream, '"scholarship":{')) {
            if (obj && obj.slug && obj.name) found.push(obj);
        }
    }
    return found;
}

// --- normalisation / filtering --------------------------------------------------

const stripHtml = (s) => (typeof s === 'string'
    ? s.replace(/<li>/gi, '\n- ').replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim()
    : null);

function normalise(s, sourceUrl) {
    const amounts = Array.isArray(s.awardAmounts) ? s.awardAmounts.filter((n) => typeof n === 'number') : [];
    const awards = Number(s.numberOfAwards ?? amounts.length) || amounts.length || null;
    const applicants = typeof s.numberOfApplicants === 'number' ? s.numberOfApplicants : null;
    const levels = (Array.isArray(s.educationLevel) ? s.educationLevel : []).map((l) => String(l).replace(/^_/, ''));
    const item = {
        name: s.name,
        slug: s.slug,
        url: `${BASE}/scholarships/${s.slug}/`,
        description: s.description || null,
        category: s.category || null,
        deadline: s.endDate || null,
        isRollingDeadline: !!s.isRollingDeadline,
        announcementDate: typeof s.announcementDate === 'string' ? s.announcementDate.replace(/^\$D/, '') : null,
        awardAmount: amounts.length ? Math.max(...amounts) : null,
        awardAmounts: amounts,
        totalAwardAmount: typeof s.totalAwardAmount === 'number' ? s.totalAwardAmount : null,
        numberOfAwards: awards,
        numberOfApplicants: applicants,
        // Competitiveness: how many applicants are chasing each award. Null when unknown.
        applicantsPerAward: applicants != null && awards ? Math.round((applicants / awards) * 10) / 10 : null,
        educationLevels: levels,
        acceptsHighSchool: !!s.acceptHighSchool,
        criteria: Array.isArray(s.criteria) ? s.criteria : [],
        requiresEssay: !!s.hasEssay,
        essayMinLength: s.essay?.minLength ?? null,
        essayMaxLength: s.essay?.maxLength ?? null,
        isMultiYear: !!s.isMultiYear,
        featured: !!s.featured,
        donorName: [s.donor?.firstName, s.donor?.lastName].filter(Boolean).join(' ').trim() || null,
        donorProfileUrl: s.donor?.profileSlug ? `${BASE}/profile/${s.donor.profileSlug}/` : null,
        donorVerified: s.donor?.verified ?? null,
        imageUrl: s.img || null,
        winnersCount: typeof s.winnersCount === 'number' ? s.winnersCount : null,
        publishedAt: typeof s.publishedAt === 'string' ? s.publishedAt.replace(/^\$D/, '') : null,
        updatedAt: typeof s.updatedAt === 'string' ? s.updatedAt.replace(/^\$D/, '') : null,
        sourceUrl,
        scrapedAt: new Date().toISOString(),
    };
    if (includeEssayPrompt) item.essayTopic = stripHtml(s.essay?.topic) || null;
    return item;
}

function keep(item) {
    if (searchTokens.length) {
        const hay = [item.name, item.description, item.category, item.slug, ...(item.criteria ?? [])]
            .filter(Boolean).join(' ').toLowerCase();
        if (!searchTokens.every((t) => hay.includes(t))) return false;
    }
    const dl = item.deadline ? Date.parse(item.deadline) : null;
    if (openOnly && !item.isRollingDeadline && dl != null && dl < Date.now()) return false;
    if (minAwardAmount != null && (item.awardAmount ?? 0) < minAwardAmount) return false;
    if (deadlineBefore != null && (dl == null || dl > deadlineBefore)) return false;
    if (deadlineAfter != null && (dl == null || dl < deadlineAfter)) return false;
    if (educationLevels.length) {
        const has = item.educationLevels.some((l) => educationLevels.includes(l.toLowerCase()))
            || (educationLevels.includes('highschool') && item.acceptsHighSchool);
        if (!has) return false;
    }
    return true;
}

// --- category discovery ---------------------------------------------------------

async function discoverCategoryUrls(types) {
    const res = await gotScraping({ url: `${BASE}/sitemap.xml`, timeout: { request: 60000 }, retry: { limit: 2 } });
    const locs = [...res.body.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
    const byType = new Map(types.map((t) => [t, []]));
    for (const u of locs) {
        for (const t of types) {
            // Require a category slug after the type: `/scholarships/by-major/` itself is a
            // hub page and carries no scholarship records.
            const m = u.match(new RegExp(`/scholarships/${t}/([^/?]+)`));
            if (m) byType.get(t).push(`${BASE}/scholarships/${t}/${m[1]}/`);
        }
    }
    // bold.org's sitemap lists the same category URL many times over (by-year: 109 <loc> entries
    // for 9 distinct categories). Without this, maxCategoryPages is spent re-fetching pages we
    // have already crawled and the run returns far fewer unique scholarships than it could.
    for (const t of types) byType.set(t, [...new Set(byType.get(t))]);
    // With a search query, crawl the category pages whose slug matches it first, so a small
    // maxCategoryPages spends its budget on relevant pages instead of alphabetical luck.
    if (searchTokens.length) {
        for (const t of types) {
            const list = byType.get(t);
            const hit = (u) => searchTokens.some((tok) => u.toLowerCase().includes(tok));
            byType.set(t, [...list.filter(hit), ...list.filter((u) => !hit(u))]);
        }
    }
    // Interleave types so a small maxCategoryPages still samples every type the user asked for.
    const out = [];
    for (let i = 0; ; i++) {
        let added = false;
        for (const t of types) {
            const list = byType.get(t);
            if (i < list.length) { out.push(list[i]); added = true; }
        }
        if (!added) break;
    }
    return out;
}

// --- main -----------------------------------------------------------------------

try {
    let urls = startUrls.length ? startUrls : await discoverCategoryUrls(categoryTypes);
    if (!startUrls.length) urls = urls.slice(0, maxCategoryPages);
    if (!urls.length) {
        log.warning('No pages to crawl. Pick at least one category type, or pass startUrls.');
        await Actor.exit();
    }
    log.info(`Crawling ${urls.length} bold.org page(s); target ${maxResults} scholarships.`);

    const seen = new Set();
    let filteredOut = 0;
    let more = true;
    for (const url of urls) {
        if (!more) break;
        const html = await fetchHtml(url);
        if (!html) continue;
        const raw = scholarshipsFromHtml(html);
        if (!raw.length) {
            log.warning(`No scholarship data found on ${url} — page layout may have changed, or it is not a scholarship page.`);
            continue;
        }
        let newOnPage = 0;
        for (const s of raw) {
            const id = String(s.id ?? s.slug);
            if (seen.has(id)) continue;
            seen.add(id);
            const item = normalise(s, url);
            if (!keep(item)) { filteredOut += 1; continue; }
            newOnPage += 1;
            more = await pushResult(item);
            if (!more) break;
        }
        log.info(`${url} -> ${raw.length} records, ${newOnPage} new after dedupe/filters (total pushed ${pushed}).`);
    }

    if (pushed === 0) {
        log.warning(
            `0 scholarships pushed. ${seen.size} record(s) were found but every one was removed by your filters `
            + `(${filteredOut} filtered out). Try clearing searchQuery / minAwardAmount / deadlineBefore / deadlineAfter / educationLevels, `
            + 'or set openOnly=false to include closed scholarships. Filtered-out records are never charged.',
        );
    }
} catch (err) {
    log.exception(err, 'Run failed');
    await Actor.fail(`Run failed: ${err.message}`);
}

log.info(`Done. Pushed ${pushed} scholarships.`);
await Actor.exit();
