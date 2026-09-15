// Substack Scraper — HTTP-only, pay-per-event.
// Uses Substack's public JSON endpoints (no login, no headless browser):
//   GET <pub>/api/v1/archive?sort=new&offset=&limit=      -> post list (metadata only, no body)
//   GET <pub>/api/v1/archive?sort=new&search=<q>&...      -> in-publication search
//   GET <pub>/api/v1/posts/<slug>                          -> single post incl. body_html
//   GET <pub>/api/v1/post/<id>/comments?all_comments=true  -> comment tree
//   GET substack.com/api/v1/categories                     -> category slugs/ids
//   GET substack.com/api/v1/category/public/<id>/all?page= -> leaderboard publications in a category
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';

await Actor.init();
// A run can fan out across many publications (URL list or category discovery) x many posts x
// per-post detail/comment fetches, all strictly sequential — heavy inputs can approach the
// platform timeout with real work still queued. Stop proactively with a safety margin and flush
// what's already collected, same pattern as google-news-scraper/shopify-products-scraper.
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
let timeBudgetExceeded = false;
let keepGoing = true;
function timeBudgetOk() {
  if (timeoutAt == null) return true;
  if (Date.now() >= timeoutAt - TIME_BUDGET_MARGIN_MS) {
    if (!timeBudgetExceeded) log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.');
    timeBudgetExceeded = true;
    keepGoing = false;
    return false;
  }
  return true;
}
const input = (await Actor.getInput()) ?? {};

const maxResults = Math.min(Number(input.maxResults ?? 200), 10000);
const maxPostsPerPublication = Math.min(Number(input.maxPostsPerPublication ?? 50), 5000);
const searchQuery = (input.searchQuery ?? '').toString().trim();
const includeBodyText = input.includeBodyText !== false;
const includeBodyHtml = input.includeBodyHtml === true;
const includeComments = input.includeComments === true;
const maxCommentsPerPost = Math.min(Number(input.maxCommentsPerPost ?? 50), 1000);
const audienceFilter = ['all', 'free', 'paid'].includes(input.audienceFilter) ? input.audienceFilter : 'all';
const publishedAfter = input.publishedAfter ? new Date(input.publishedAfter) : null;
const publishedBefore = input.publishedBefore ? new Date(input.publishedBefore) : null;
const discoverCategories = (input.discoverCategories ?? []).map((c) => String(c ?? '').trim()).filter(Boolean);
const maxPublicationsPerCategory = Math.min(Number(input.maxPublicationsPerCategory ?? 10), 100);
const discoverType = ['all', 'newsletter', 'podcast'].includes(input.discoverType) ? input.discoverType : 'all';

// Posts that come back without an article body are cheaper for us (no per-post detail request)
// and are billed on their own, cheaper event — see the Pricing section of README.md.
const POST_EVENT = includeBodyText || includeBodyHtml ? 'result' : 'post-metadata';

const cm = Actor.getChargingManager();
const isPPE = cm.getPricingInfo().isPayPerEvent;
let pushed = 0;
let excludedByFilters = 0;
const filtersActive = audienceFilter !== 'all' || !!publishedAfter || !!publishedBefore;

async function pushResult(item, eventName = 'result') {
  if (isPPE) {
    const r = await Actor.charge({ eventName, count: 1 });
    if (r.chargedCount === 0) return false; // budget exhausted: never push unpaid items
    await Actor.pushData(item); pushed += 1;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  return pushed < maxResults;
}

async function getJson(url) {
  const res = await gotScraping({
    url,
    timeout: { request: 45000 },
    retry: { limit: 3, statusCodes: [408, 413, 429, 500, 502, 503, 504] },
    responseType: 'json',
    followRedirect: true, // <handle>.substack.com often 301s to a custom domain
    headers: { accept: 'application/json' },
  });
  return res.body;
}

// "acme", "acme.substack.com", "https://www.acme.com/p/post-slug" -> { origin, postSlug }
function parseTarget(raw) {
  let s = String(raw ?? '').trim();
  if (!s) return null;
  s = s.replace(/^@/, '');
  if (!/^https?:\/\//i.test(s)) s = `https://${s.includes('.') ? s : `${s}.substack.com`}`;
  let u;
  try { u = new URL(s); } catch { return null; }
  const m = u.pathname.match(/^\/p\/([^/?#]+)/);
  return { origin: u.origin, postSlug: m ? m[1] : null };
}

function htmlToText(html) {
  if (!html) return null;
  const $ = cheerio.load(html);
  $('script, style').remove();
  $('p, div, br, li, h1, h2, h3, h4, h5, h6, blockquote').after('\n');
  return $.root().text().replace(/ /g, ' ').replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n').trim() || null;
}

function matchesAudience(post) {
  const paid = post.audience && post.audience !== 'everyone';
  if (audienceFilter === 'free') return !paid;
  if (audienceFilter === 'paid') return !!paid;
  return true;
}

function matchesDate(post) {
  if (!publishedAfter && !publishedBefore) return true;
  const d = post.post_date ? new Date(post.post_date) : null;
  if (!d || Number.isNaN(d.getTime())) return true;
  if (publishedAfter && d < publishedAfter) return false;
  if (publishedBefore && d > publishedBefore) return false;
  return true;
}

function mapPost(post, origin, detail) {
  const full = detail ?? post;
  const bodyHtml = full.body_html || null;
  const bodyText = htmlToText(bodyHtml) ?? (post.truncated_body_text || null);
  const url = post.canonical_url || `${origin}/p/${post.slug}`;
  return {
    type: 'post',
    id: post.id,
    title: post.title ?? null,
    subtitle: post.subtitle ?? null,
    slug: post.slug ?? null,
    url,
    publicationUrl: origin,
    publicationId: post.publication_id ?? null,
    publicationName: (post.publishedBylines ?? full.publishedBylines ?? [])
      .flatMap((b) => b.publicationUsers ?? [])
      .map((pu) => pu.publication?.name)
      .find(Boolean) ?? null,
    authors: (post.publishedBylines ?? []).map((b) => b.name).filter(Boolean),
    postDate: post.post_date ?? null,
    audience: post.audience ?? null,
    isPaid: !!(post.audience && post.audience !== 'everyone'),
    postType: post.type ?? null,
    wordCount: full.wordcount ?? post.wordcount ?? null,
    reactionCount: post.reaction_count ?? 0,
    commentCount: post.comment_count ?? 0,
    restackCount: post.restacks ?? 0,
    description: post.description ?? null,
    coverImage: post.cover_image ?? null,
    section: post.section_name ?? null,
    tags: (post.postTags ?? []).map((t) => t.name).filter(Boolean),
    podcastUrl: post.podcast_url ?? null,
    podcastDurationSec: post.podcast_duration ?? null,
    language: post.language ?? null,
    bodyText: includeBodyText ? bodyText : undefined,
    bodyHtml: includeBodyHtml ? bodyHtml : undefined,
    // true when the full article text is not publicly available (paywalled subscriber-only post)
    bodyTruncated: includeBodyText ? !bodyText : undefined,
  };
}

function flattenComments(nodes, out = []) {
  for (const c of nodes ?? []) {
    out.push(c);
    if (c.children?.length) flattenComments(c.children, out);
  }
  return out;
}

function mapComment(c, post, origin) {
  return {
    type: 'comment',
    id: c.id,
    postId: post.id,
    postTitle: post.title ?? null,
    postUrl: post.canonical_url || `${origin}/p/${post.slug}`,
    publicationUrl: origin,
    parentCommentId: c.ancestor_path ? Number(String(c.ancestor_path).split('.').filter(Boolean).pop()) || null : null,
    author: c.name ?? null,
    authorHandle: c.handle ?? null,
    body: c.body ?? null,
    date: c.date ?? null,
    reactionCount: c.reaction_count ?? 0,
    restackCount: c.restacks ?? 0,
    replyCount: c.children_count ?? 0,
    isDeleted: !!c.deleted,
  };
}

async function fetchDetail(origin, slug) {
  try {
    return await getJson(`${origin}/api/v1/posts/${encodeURIComponent(slug)}`);
  } catch (e) {
    log.warning(`Could not fetch full post ${origin}/p/${slug}: ${e.message}`);
    return null;
  }
}

async function handlePost(post, origin, preloadedDetail = null) {
  if (!matchesAudience(post) || !matchesDate(post)) { excludedByFilters += 1; return true; }
  const needDetail = includeBodyText || includeBodyHtml;
  const detail = preloadedDetail ?? (needDetail && post.slug ? await fetchDetail(origin, post.slug) : null);
  keepGoing = await pushResult(mapPost(post, origin, detail), POST_EVENT);
  if (!keepGoing) return false;

  if (includeComments && (post.comment_count ?? 0) > 0 && timeBudgetOk()) {
    try {
      const body = await getJson(`${origin}/api/v1/post/${post.id}/comments?token=&all_comments=true&sort=best_first`);
      const flat = flattenComments(body.comments).slice(0, maxCommentsPerPost);
      for (const c of flat) {
        keepGoing = await pushResult(mapComment(c, post, origin), 'comment');
        if (!keepGoing) return false;
      }
    } catch (e) {
      log.warning(`Comments failed for post ${post.id}: ${e.message}`);
    }
  }
  return keepGoing;
}

// Returns 'ok' | 'empty' (archive has no matching posts) | 'filtered' (posts exist but
// audienceFilter/publishedAfter/publishedBefore excluded all of them) | 'error' (archive request failed).
async function scrapePublication(origin) {
  log.info(`Publication: ${origin}${searchQuery ? ` (search: "${searchQuery}")` : ''}`);
  let offset = 0;
  let seen = 0;
  const pageSize = 50;
  const pushedBefore = pushed;
  const excludedBefore = excludedByFilters;
  let requestFailed = false;
  while (keepGoing && seen < maxPostsPerPublication && timeBudgetOk()) {
    const url = new URL(`${origin}/api/v1/archive`);
    url.searchParams.set('sort', 'new');
    if (searchQuery) url.searchParams.set('search', searchQuery);
    url.searchParams.set('offset', String(offset));
    url.searchParams.set('limit', String(Math.min(pageSize, maxPostsPerPublication - seen)));
    let posts;
    try {
      posts = await getJson(url.toString());
    } catch (e) {
      log.warning(`Archive request failed for ${origin} (offset ${offset}): ${e.message}`);
      requestFailed = true;
      break;
    }
    if (!Array.isArray(posts) || !posts.length) break;
    for (const post of posts) {
      seen += 1;
      if (!(await handlePost(post, origin))) return pushed > pushedBefore ? 'ok' : 'filtered';
      if (seen >= maxPostsPerPublication) break;
    }
    offset += posts.length;
  }
  if (requestFailed && seen === 0) return 'error';
  if (seen === 0) return 'empty';
  // Depth cap reached with filters discarding posts: whatever sits deeper in the archive was
  // never looked at, so the result set is truncated by the cap rather than by the filters.
  if (seen >= maxPostsPerPublication && excludedByFilters > excludedBefore) {
    const dropped = excludedByFilters - excludedBefore;
    log.warning(
      `${origin}: scanned the maxPostsPerPublication limit of ${maxPostsPerPublication} post(s) and `
      + `${dropped} of them were excluded by audienceFilter/publishedAfter/publishedBefore. `
      + `The cap counts posts scanned, before filtering — raise maxPostsPerPublication to search deeper.`,
    );
    depthCapped.push(origin);
  }
  return pushed > pushedBefore ? 'ok' : 'filtered';
}

// Category discovery: turn "technology"/"finance"/... into publication origins, ranked by
// Substack's own leaderboard order, so a run can start from a topic instead of a URL list.
async function resolveCategoryIds(wanted) {
  let cats;
  try {
    cats = await getJson('https://substack.com/api/v1/categories');
  } catch (e) {
    log.warning(`Could not load Substack category list: ${e.message}`);
    return [];
  }
  const flat = [];
  for (const c of Array.isArray(cats) ? cats : []) {
    flat.push(c);
    for (const s of c.subcategories ?? []) flat.push(s);
  }
  const bySlug = new Map();
  for (const c of flat) {
    if (c.slug) bySlug.set(String(c.slug).toLowerCase(), c);
    if (c.name) bySlug.set(String(c.name).toLowerCase(), c);
    if (c.id != null) bySlug.set(String(c.id), c);
  }
  const out = [];
  for (const w of wanted) {
    const hit = bySlug.get(w.toLowerCase());
    if (hit) out.push({ id: hit.id, slug: hit.slug ?? String(hit.id) });
    else log.warning(`Unknown category "${w}" — skipped. Valid slugs come from substack.com/api/v1/categories (e.g. technology, business, finance, culture).`);
  }
  return out;
}

async function discoverPublications(cat) {
  const found = [];
  const pageSize = 25;
  for (let page = 0; found.length < maxPublicationsPerCategory && timeBudgetOk(); page += 1) {
    const url = `https://substack.com/api/v1/category/public/${cat.id}/all?page=${page}&limit=${pageSize}`;
    let body;
    try {
      body = await getJson(url);
    } catch (e) {
      log.warning(`Category "${cat.slug}" page ${page} failed: ${e.message}`);
      break;
    }
    const pubs = body?.publications;
    if (!Array.isArray(pubs) || !pubs.length) break;
    for (const p of pubs) {
      if (discoverType !== 'all' && p.type && p.type !== discoverType) continue;
      const host = p.custom_domain || (p.subdomain ? `${p.subdomain}.substack.com` : null);
      if (!host) continue;
      found.push({ origin: `https://${host}`, postSlug: null, name: p.name, category: cat.slug });
      if (found.length >= maxPublicationsPerCategory) break;
    }
    if (!body.more) break;
  }
  log.info(`Category "${cat.slug}": discovered ${found.length} publication(s)${found.length ? ` — ${found.slice(0, 5).map((f) => f.name).join(', ')}${found.length > 5 ? ', …' : ''}` : ''}`);
  return found;
}

const publicationTargets = [];
const postTargets = [];
for (const raw of input.publicationUrls ?? []) {
  const t = parseTarget(raw);
  if (t) (t.postSlug ? postTargets : publicationTargets).push(t);
}
for (const raw of input.postUrls ?? []) {
  const t = parseTarget(raw);
  if (t?.postSlug) postTargets.push(t);
  else if (t) publicationTargets.push(t);
}
let unknownCategories = false;
if (discoverCategories.length) {
  const cats = await resolveCategoryIds(discoverCategories);
  unknownCategories = cats.length === 0;
  for (const cat of cats) {
    if (!timeBudgetOk()) break;
    publicationTargets.push(...(await discoverPublications(cat)));
  }
}
// A publication can be reached by handle and by custom domain, and can sit in two categories.
const seenOrigins = new Set();
const dedupedPublications = publicationTargets.filter((t) => {
  if (seenOrigins.has(t.origin)) return false;
  seenOrigins.add(t.origin);
  return true;
});
publicationTargets.length = 0;
publicationTargets.push(...dedupedPublications);
// Same post reachable via handle or custom domain, or just pasted twice — dedup before fetching
// so a duplicate postUrls entry doesn't fetch and charge for the same post twice.
const seenPosts = new Set();
const dedupedPosts = postTargets.filter((t) => {
  const key = `${t.origin}/p/${t.postSlug}`;
  if (seenPosts.has(key)) return false;
  seenPosts.add(key);
  return true;
});
postTargets.length = 0;
postTargets.push(...dedupedPosts);

const errored = [];
const empty = [];
const filtered = [];
// Publications where the maxPostsPerPublication depth cap was reached while filters were
// dropping posts — the user is silently seeing fewer results than actually match.
const depthCapped = [];

if (!publicationTargets.length && !postTargets.length) {
  const why = unknownCategories
    ? 'none of the discoverCategories matched a Substack category — use a slug from substack.com/api/v1/categories (e.g. technology, business, finance)'
    : discoverCategories.length
      ? 'category discovery returned no publications — try a different category or raise maxPublicationsPerCategory'
      : 'no publicationUrls, postUrls or discoverCategories were provided';
  log.warning(`Nothing to do — ${why}.`);
  await Actor.setStatusMessage(`No items returned — ${why}.`);
} else {
  for (const t of postTargets) {
    if (!keepGoing) break;
    const label = t.origin && t.postSlug ? `${t.origin}/p/${t.postSlug}` : t.origin;
    const detail = await fetchDetail(t.origin, t.postSlug);
    if (!detail) { errored.push(label); continue; }
    const pushedBefore = pushed;
    if (!(await handlePost(detail, t.origin, detail))) break;
    if (pushed === pushedBefore) filtered.push(label);
  }
  for (const t of publicationTargets) {
    if (!keepGoing) break;
    const result = await scrapePublication(t.origin);
    if (result === 'error') errored.push(t.origin);
    else if (result === 'empty') empty.push(t.origin);
    else if (result === 'filtered') filtered.push(t.origin);
  }

  const timeBudgetNote = timeBudgetExceeded
    ? 'stopped early, approaching the run timeout — narrow publicationUrls/discoverCategories or lower maxPostsPerPublication/maxPublicationsPerCategory to get a complete run'
    : null;
  if (pushed === 0 && (publicationTargets.length || postTargets.length)) {
    const why = timeBudgetNote
      ? timeBudgetNote
      : errored.length
        ? `the request failed for: ${errored.join(', ')} (see log for the error — check the publication/post URL is correct)`
        : filtered.length && !empty.length
          ? `every post matching ${filtered.join(', ')} was excluded by audienceFilter/publishedAfter/publishedBefore — try widening those filters`
          : `no posts were found for: ${empty.concat(filtered).join(', ')} — the publication may be empty, private, or the URL/handle is wrong`;
    await Actor.setStatusMessage(`No items returned — ${why}.`);
  } else if (errored.length || empty.length || filtered.length || depthCapped.length || timeBudgetNote) {
    const notes = [];
    if (timeBudgetNote) notes.push(timeBudgetNote);
    if (errored.length) notes.push(`request failed for ${errored.join(', ')}`);
    if (empty.length) notes.push(`no posts found for ${empty.join(', ')}`);
    if (filtered.length) notes.push(`filters excluded everything from ${filtered.join(', ')}`);
    if (depthCapped.length) {
      notes.push(
        `hit maxPostsPerPublication (${maxPostsPerPublication}) while filtering ${depthCapped.join(', ')}`
        + ` — the cap counts posts scanned before filters, so raise it to search deeper`,
      );
    }
    await Actor.setStatusMessage(`Pushed ${pushed} items. ${notes.join('; ')}.`);
  }
}

log.info(`Done. Pushed ${pushed} items.`);
await Actor.exit();
