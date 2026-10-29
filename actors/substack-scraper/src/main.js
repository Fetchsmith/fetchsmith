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
// Milliseconds of useful work left before the margin starts. Infinity on a local/dev run, where
// the platform sets no deadline.
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
function timeBudgetOk() {
  if (remainingMs() <= 0) {
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
const includePublicationInfo = input.includePublicationInfo === true;
const maxCommentsPerPost = Math.min(Number(input.maxCommentsPerPost ?? 50), 1000);
const audienceFilter = ['all', 'free', 'paid'].includes(input.audienceFilter) ? input.audienceFilter : 'all';
const contentType = ['all', 'newsletter', 'podcast', 'thread'].includes(input.contentType) ? input.contentType : 'all';
// Live-checked 2026-09-29 across a dozen large, active publications spanning news, tech, culture,
// comedy, economics and Substack's own in-house blog: every post returned by the archive API this
// Actor reads was type "newsletter" or "podcast", including posts titled "Open Thread" — Substack
// Notes/threads live on a separate surface (substack.com/notes) this endpoint never exposes. Kept
// selectable (harmless, and a future publication or Substack feature could change this) but a
// buyer who picks it deserves to know it matched nothing in every publication tested so far.
if (contentType === 'thread') {
  log.warning('contentType="thread" requested — as of 2026-09-29, no publication we tested (spanning several genres and sizes) had any post of type "thread" in Substack\'s archive API; every post was "newsletter" or "podcast". Substack Notes/threads are a separate product surface this Actor does not fetch, so this filter is very likely to return 0 rows here too. Use contentType="all" and check the postType field on your results if you need to confirm.');
}
// A malformed value must not reach matchesDate() below as an `Invalid Date`: Invalid Date is
// truthy, so the `publishedAfter && d < publishedAfter` guard would pass while the comparison
// itself is always false (NaN semantics) — BOTH bounds silently defeated for every row, same
// widen-and-bill defect class as sinceDate/clinicaltrials-scraper's date filters. Throw instead,
// matching the fleet's dominant convention for this input shape.
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
function parseDateBound(raw, fieldName) {
  const s = String(raw ?? '').trim();
  if (!s) return null;
  if (!DATE_RE.test(s)) {
    throw new Error(`"${fieldName}" must be YYYY-MM-DD (got ${JSON.stringify(raw)}). An unparseable date here used to be silently ignored, matching every post regardless of this filter.`);
  }
  return new Date(s);
}
const publishedAfter = parseDateBound(input.publishedAfter, 'publishedAfter');
const publishedBefore = parseDateBound(input.publishedBefore, 'publishedBefore');
const minReactionCount = input.minReactionCount != null ? Number(input.minReactionCount) : null;
const minCommentCount = input.minCommentCount != null ? Number(input.minCommentCount) : null;
const minRestackCount = input.minRestackCount != null ? Number(input.minRestackCount) : null;
const minWordCount = input.minWordCount != null ? Number(input.minWordCount) : null;
const maxWordCount = input.maxWordCount != null ? Number(input.maxWordCount) : null;
const discoverCategories = (input.discoverCategories ?? []).map((c) => String(c ?? '').trim()).filter(Boolean);
const maxPublicationsPerCategory = Math.min(Number(input.maxPublicationsPerCategory ?? 10), 100);
const discoverType = ['all', 'newsletter', 'podcast'].includes(input.discoverType) ? input.discoverType : 'all';
const requirePodcast = input.requirePodcast === true;
const requirePaymentsEnabled = input.requirePaymentsEnabled === true;
function attrFilterLabel() {
  const parts = [];
  if (requirePodcast) parts.push('requirePodcast');
  if (requirePaymentsEnabled) parts.push('requirePaymentsEnabled');
  return parts.map((p) => `${p}=true`).join(' and ');
}
const leaderboardTier = ['all', 'free', 'paid'].includes(input.leaderboardTier) ? input.leaderboardTier : 'all';
const leaderboardOnly = input.leaderboardOnly === true;

// Posts that come back without an article body are cheaper for us (no per-post detail request)
// and are billed on their own, cheaper event — see the Pricing section of README.md.
const POST_EVENT = includeBodyText || includeBodyHtml ? 'result' : 'post-metadata';

const cm = Actor.getChargingManager();
const isPPE = cm.getPricingInfo().isPayPerEvent;
let pushed = 0;
let excludedByFilters = 0;
// Posts where Substack acknowledged comments exist (`comment_count > 0`) but served an empty
// comment tree. Subscriber-only posts keep their comment section behind the paywall and the
// endpoint answers 200 with `comments: []` rather than an error — see commentsWithheld below.
let postsWithCommentsWithheld = 0;
const filtersActive = audienceFilter !== 'all' || contentType !== 'all' || !!publishedAfter || !!publishedBefore
  || minReactionCount != null || minCommentCount != null || minRestackCount != null || minWordCount != null || maxWordCount != null;

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

// got applies `timeout.request` PER ATTEMPT, so `retry.limit: 3` was worth up to 4x45s = 180s in
// a single call — far more than the TIME_BUDGET_MARGIN_MS the between-request timeBudgetOk()
// checks leave, which is how one real external run TIMED-OUT (google-news-scraper, cycle 712;
// same copied pattern here). Clamp both the per-attempt timeout and the retry count to what's
// actually left so no single call can outlive the run.
const MIN_REQUEST_MS = 3000; // below this a request is not worth starting; stop instead
async function getJson(url) {
  const left = remainingMs();
  if (left <= MIN_REQUEST_MS) { timeBudgetExceeded = true; throw new Error('run time budget exhausted before the request could be made'); }
  const perRequest = Math.max(MIN_REQUEST_MS, Math.min(45000, left));
  const retryLimit = Math.max(0, Math.min(3, Math.floor(left / perRequest) - 1));
  const res = await gotScraping({
    url,
    timeout: { request: perRequest },
    retry: { limit: retryLimit, statusCodes: [408, 413, 429, 500, 502, 503, 504] },
    responseType: 'json',
    followRedirect: true, // <handle>.substack.com often 301s to a custom domain
    headers: { accept: 'application/json' },
  });
  return res.body;
}

// Publication-level metadata (subscriber count, author, plan prices, podcast flags) is not on any
// JSON endpoint — /api/v1/publication is owner-only (403 "Not authorized") — but the publication
// homepage embeds it in `window._preloads`. One extra HTML request per publication, opt-in via
// includePublicationInfo, cached per origin so a 50-post run still costs exactly one fetch.
// Deliberately NOT extracted: support_email / email_from (contact details, PII rule).
const pubInfoCache = new Map();

function parsePlans(plans) {
  const out = [];
  for (const p of plans ?? []) {
    if (!p?.active || typeof p.amount !== 'number') continue;
    out.push({
      interval: p.interval ?? null,
      intervalCount: p.interval_count ?? 1,
      amount: p.amount / 100,
      currency: (p.currency ?? 'usd').toUpperCase(),
      name: p.nickname ?? null,
    });
  }
  return out;
}

function mapPublicationInfo(pub) {
  // freeSubscriberCount arrives as a display string ("156,000"); keep a numeric form too.
  const rawCount = pub.freeSubscriberCount ?? null;
  const numericCount = rawCount ? Number(String(rawCount).replace(/[^0-9]/g, '')) || null : null;
  return {
    publicationSubscriberCount: numericCount,
    publicationSubscriberCountLabel: pub.rankingDetailFreeSubscriberCount ?? rawCount ?? null,
    publicationPaidSubscribersLabel: pub.rankingDetail ?? null,
    publicationBestsellerTier: pub.author_bestseller_tier ?? null,
    publicationAuthorName: pub.author_name ?? null,
    publicationAuthorHandle: pub.author_handle ?? null,
    publicationAuthorBio: pub.author_bio || null,
    publicationDescription: pub.hero_text || null,
    publicationType: pub.type ?? null,
    publicationLanguage: pub.language ?? null,
    publicationFirstPostDate: pub.first_post_date ?? null,
    publicationHasPodcast: pub.podcast_enabled ?? pub.has_podcast ?? null,
    publicationInviteOnly: pub.invite_only ?? null,
    publicationPaymentsEnabled: pub.payments_state ? pub.payments_state === 'enabled' : null,
    publicationPlans: parsePlans(pub.plans),
    publicationLogoUrl: pub.logo_url ?? null,
  };
}

// Every field null (rather than an absent key) when the fetch or the parse fails, so the dataset
// keeps a stable shape and a partial run is still usable.
const EMPTY_PUB_INFO = mapPublicationInfo({});

// This is opt-in supplementary metadata (fields null-on-failure, never the row itself), fetched
// once per origin and cached — but it sits ahead of the first `pushResult` for that origin's first
// post. Routing it through `getJson`'s budget-proportional retry ladder (up to ~2 retries at up to
// 45s each) meant one flaky publication homepage could burn well over half the run's remaining
// budget before a single row was pushed — the same "optional call on the load-bearing ladder" shape
// fixed in shopify-products-scraper's `currencyFor` (cycle 992). Same fix: one attempt, hard capped,
// skipped outright when the budget is thin.
const PUB_INFO_MAX_MS = 8000;
async function fetchPublicationInfo(origin) {
  if (!includePublicationInfo) return null;
  if (pubInfoCache.has(origin)) return pubInfoCache.get(origin);
  let info = EMPTY_PUB_INFO;
  if (remainingMs() <= PUB_INFO_MAX_MS + MIN_REQUEST_MS) {
    pubInfoUnavailable.add(origin);
    log.warning(`${origin}: skipping the publication-info lookup — not enough run time left to spend on it. The publicationXxx fields will be null for this publication's rows; post content itself is unaffected.`);
    pubInfoCache.set(origin, info);
    return info;
  }
  try {
    const res = await gotScraping({
      url: `${origin}/`,
      timeout: { request: PUB_INFO_MAX_MS },
      retry: { limit: 0 },
      followRedirect: true,
      headers: { accept: 'text/html' },
    });
    // Substack moved the payload out of the inline `JSON.parse("...")` string literal into its
    // own `<script id="preloads-json" type="application/json">{...}</script>` tag (observed live
    // 2026-10-19 on astralcodexten — the old inline form is now just a `document.querySelector(...)`
    // call with no quoted JSON for the old regex to catch, which silently null-filled every
    // publicationXxx field on every run). Try the current tag-based form first, fall back to the
    // old inline form in case some publications still serve it.
    const body = String(res.body);
    const tagMatch = body.match(/<script[^>]*id=["']preloads-json["'][^>]*>(.*?)<\/script>/s);
    const inlineMatch = body.match(/window\._preloads\s*=\s*JSON\.parse\("(.*?)"\)\s*<\/script>/s);
    const pub = tagMatch
      ? JSON.parse(tagMatch[1])?.pub
      : inlineMatch
        ? JSON.parse(JSON.parse(`"${inlineMatch[1]}"`))?.pub
        : null;
    if (pub) info = mapPublicationInfo(pub);
    else {
      pubInfoUnavailable.add(origin);
      log.warning(`Publication info not found in the homepage of ${origin} — returning null fields.`);
    }
  } catch (e) {
    pubInfoUnavailable.add(origin);
    log.warning(`Publication info failed for ${origin}: ${e.message} — returning null fields.`);
  }
  pubInfoCache.set(origin, info);
  return info;
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

// Substack serves a *free preview* of a subscriber-only post to logged-out clients: body_html is
// present but cut off mid-article, while the post's `wordcount` still reports the full length. A
// non-empty body is therefore NOT proof of a complete article, so `bodyTruncated` cannot just be
// `!bodyText` — compare what we actually extracted against the declared word count.
// Re-measured cycle 740 at n=69 over 7 publications (write-up: /blog/substack-paywalled-post-preview-vs-full-text):
//   free  (n=42): ratio 0.976–1.402, median 1.007 — 0 falsely flagged at the 0.9 threshold.
//   paid  (n=27): ratio 0.000–0.967, median 0.337. Preview length is a per-publication setting
//                 (experimentalhistory 0.02–0.05, noahpinion 0.25–0.37, doomberg 0.34–0.46).
// `audience` is NOT a usable substitute for this check: 4/27 paid posts came back essentially whole
// (0.959–0.967) because publications unlock posts without changing the flag. Extraction also
// routinely OVERSHOOTS `wordcount` (captions/footnotes/embeds), which is why the threshold is a
// floor on what is missing, not an equality test.
const BODY_COMPLETE_RATIO = 0.9;
// Absolute floor so a short post whose tokenisation differs slightly from Substack's isn't flagged
// (smallest real preview shortfall measured: 1185 words).
const BODY_SHORTFALL_MIN_WORDS = 50;

function countWords(text) {
  if (!text) return 0;
  return text.split(/\s+/).filter(Boolean).length;
}

function isBodyTruncated(bodyText, bodyWordCount, declaredWordCount) {
  if (!bodyText) return true;
  if (typeof declaredWordCount !== 'number' || !Number.isFinite(declaredWordCount) || declaredWordCount <= 0) return false;
  const shortfall = declaredWordCount - bodyWordCount;
  return shortfall >= BODY_SHORTFALL_MIN_WORDS && bodyWordCount < declaredWordCount * BODY_COMPLETE_RATIO;
}

function matchesAudience(post) {
  const paid = post.audience && post.audience !== 'everyone';
  if (audienceFilter === 'free') return !paid;
  if (audienceFilter === 'paid') return !!paid;
  return true;
}

function matchesContentType(post) {
  if (contentType === 'all') return true;
  return post.type === contentType;
}

function matchesDate(post) {
  if (!publishedAfter && !publishedBefore) return true;
  const d = post.post_date ? new Date(post.post_date) : null;
  if (!d || Number.isNaN(d.getTime())) return true;
  if (publishedAfter && d < publishedAfter) return false;
  if (publishedBefore && d > publishedBefore) return false;
  return true;
}

// reaction/comment/restack/word counts are all already on the archive-listing object itself
// (Substack includes them in the list response, not just the per-post detail endpoint), so these
// filters apply before any post is fetched or charged — same cost as no filter at all.
function matchesEngagement(post) {
  if (minReactionCount != null && (post.reaction_count ?? 0) < minReactionCount) return false;
  if (minCommentCount != null && (post.comment_count ?? 0) < minCommentCount) return false;
  if (minRestackCount != null && (post.restacks ?? 0) < minRestackCount) return false;
  const wc = post.wordcount;
  if ((minWordCount != null || maxWordCount != null) && typeof wc === 'number') {
    if (minWordCount != null && wc < minWordCount) return false;
    if (maxWordCount != null && wc > maxWordCount) return false;
  }
  return true;
}

function mapPost(post, origin, detail, pubInfo, commentFetch) {
  const full = detail ?? post;
  const bodyHtml = full.body_html || null;
  const bodyText = htmlToText(bodyHtml) ?? (post.truncated_body_text || null);
  const url = post.canonical_url || `${origin}/p/${post.slug}`;
  const declaredWordCount = full.wordcount ?? post.wordcount ?? null;
  const bodyWordCount = countWords(bodyText);
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
    // cycle 1525 enum_audit: a publication's own archive can include "restack" entries (it
    // reshared someone else's post) alongside its real newsletter/podcast posts — not a
    // contentType value we expose, and contentType="all" (the default) does not filter it out.
    // When includeBodyText/includeBodyHtml fetch the per-post detail for one of these, Substack
    // resolves it straight through to the ORIGINAL post's full body, so the content attached to
    // this row is the restacked publication's writing, not this origin's — flag it rather than
    // let it pass as this publication's own content.
    isRestack: post.type === 'restack',
    wordCount: declaredWordCount,
    reactionCount: post.reaction_count ?? 0,
    commentCount: post.comment_count ?? 0,
    restackCount: post.restacks ?? 0,
    description: post.description ?? null,
    coverImage: post.cover_image ?? null,
    section: post.section_name ?? null,
    tags: (post.postTags ?? []).map((t) => t.name).filter(Boolean),
    podcastUrl: post.podcast_url ?? null,
    podcastDurationSec: post.podcast_duration != null ? Math.round(post.podcast_duration) : null,
    language: post.language ?? null,
    bodyText: includeBodyText ? bodyText : undefined,
    bodyHtml: includeBodyHtml ? bodyHtml : undefined,
    // How many words of body we actually extracted, vs. `wordCount` which is the full article's
    // length as Substack reports it. They match on public posts and diverge on paywalled previews.
    bodyWordCount: includeBodyText ? bodyWordCount : undefined,
    // true when the text returned is not the complete article — either no public body at all, or
    // only the free preview of a subscriber-only post.
    bodyTruncated: includeBodyText ? isBodyTruncated(bodyText, bodyWordCount, declaredWordCount) : undefined,
    // How many comments Substack actually handed back for this post, vs. `commentCount` which is
    // the total it says the post has. `null` means we could not find out (the request failed, or
    // the run ran out of time before asking). Not affected by maxCommentsPerPost — that cap is
    // your own, and applies after this count.
    commentsRetrieved: includeComments ? (commentFetch ? commentFetch.comments.length : null) : undefined,
    // true when the post has comments but Substack served none of them: subscriber-only posts keep
    // their comment section paywalled, and the API says so with an empty list, not an error.
    commentsWithheld: includeComments
      ? (commentFetch ? commentFetch.comments.length === 0 && (post.comment_count ?? 0) > 0 : null)
      : undefined,
    ...(pubInfo ?? {}),
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

// Returns `{ comments: [...] }` when we know what Substack has (possibly an empty list — that is
// itself the answer on a paywalled comment section), or `null` when we could not find out. The
// caller needs that distinction to report commentsRetrieved/commentsWithheld honestly, which is
// why this runs before the post row is pushed rather than after.
async function fetchComments(origin, post) {
  if (!includeComments) return null;
  if ((post.comment_count ?? 0) === 0) return { comments: [] };
  if (!timeBudgetOk()) return null;
  try {
    const body = await getJson(`${origin}/api/v1/post/${post.id}/comments?token=&all_comments=true&sort=best_first`);
    return { comments: flattenComments(body.comments) };
  } catch (e) {
    log.warning(`Comments failed for post ${post.id}: ${e.message}`);
    return null;
  }
}

async function handlePost(post, origin, preloadedDetail = null) {
  if (!matchesAudience(post) || !matchesContentType(post) || !matchesDate(post) || !matchesEngagement(post)) { excludedByFilters += 1; return true; }
  const needDetail = includeBodyText || includeBodyHtml;
  const detail = preloadedDetail ?? (needDetail && post.slug ? await fetchDetail(origin, post.slug) : null);
  const pubInfo = await fetchPublicationInfo(origin);
  const commentFetch = await fetchComments(origin, post);
  if (commentFetch && commentFetch.comments.length === 0 && (post.comment_count ?? 0) > 0) {
    postsWithCommentsWithheld += 1;
    log.warning(
      `Substack served 0 of ${post.comment_count} comments for ${origin}/p/${post.slug}`
      + ' — subscriber-only posts keep their comment section paywalled. Row flagged commentsWithheld:true.',
    );
  }
  keepGoing = await pushResult(mapPost(post, origin, detail, pubInfo, commentFetch), POST_EVENT);
  if (!keepGoing) return false;

  for (const c of (commentFetch?.comments ?? []).slice(0, maxCommentsPerPost)) {
    keepGoing = await pushResult(mapComment(c, post, origin), 'comment');
    if (!keepGoing) return false;
  }
  // fetchComments() now runs BEFORE the post row is pushed, so a time budget it tripped would be
  // overwritten by pushResult()'s return value above. Re-assert it, or the run would carry on past
  // the timeout margin (the pre-reorder code got this for free by pushing the post row first).
  if (timeBudgetExceeded) keepGoing = false;
  return keepGoing;
}

// Returns 'ok' | 'empty' (archive has no matching posts) | 'filtered' (posts exist but
// audienceFilter/contentType/date/engagement filters excluded all of them) | 'error' (archive request failed).
async function scrapePublication(origin) {
  log.info(`Publication: ${origin}${searchQuery ? ` (search: "${searchQuery}")` : ''}`);
  let offset = 0;
  let seen = 0;
  // Keep at 50 or below. Substack honours `limit` only loosely: at offset 0 any limit from 25 to 50
  // comes back truncated to 23 items (verified cycle 1048 on 3 publications), and `limit=100`
  // degenerates to a single item — so raising this to "fewer round trips" would instead paginate one
  // post at a time. The `offset += posts.length` below is what keeps paging correct regardless.
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
      const landedOnProfile = /^https:\/\/substack\.com\/@/.test(e.response?.url ?? '');
      if (landedOnProfile) {
        log.warning(
          `Archive request failed for ${origin} (offset ${offset}): redirected to a Substack `
          + `profile page (${e.response.url}) instead of the archive — this publication's bare `
          + 'handle no longer resolves to its own archive; find its real custom domain or '
          + '"<handle>.substack.com" homepage URL and pass that instead.',
        );
        profileRedirected.push(origin);
      } else {
        log.warning(`Archive request failed for ${origin} (offset ${offset}): ${e.message}`);
      }
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
      + `${dropped} of them were excluded by audienceFilter/contentType/publishedAfter/publishedBefore/min-max filters. `
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
    // Not the same thing as a bad slug: both end up with zero resolved categories, but the old
    // single `unknownCategories` flag told the buyer to go find a valid slug, which cannot help
    // when substack.com/api/v1/categories itself is what failed. Re-running is the real remedy.
    categoryListFailed = e.message;
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
    else {
      unknownCategorySlugs.push(w);
      log.warning(`Unknown category "${w}" — skipped. Valid slugs come from substack.com/api/v1/categories (e.g. technology, business, finance, culture).`);
    }
  }
  return out;
}

// Substack ranks publications in 3 separate lists per category (overall/free/paid) at
// category/public/<id>/<tier> — same publication object shape as the homepage's window._preloads
// (verified live), so a leaderboard hit is also a complete, free includePublicationInfo profile.
// Substack's category leaderboards are overwhelmingly `newsletter` publications — a live sweep of
// the whole technology leaderboard (300 publications, 12 pages, both the `all` and `paid` tiers)
// found zero `podcast`-type ones, and even the dedicated `podcast` category is only ~3% podcast.
// So discoverType:'podcast' legitimately returns nothing for most categories; count what the filter
// dropped so the zero-row remedy can name it instead of pointing at maxPublicationsPerCategory.
let discoverTypeSkipped = 0;
// requirePodcast/requirePaymentsEnabled read the same leaderboard publication object discoverType
// already reads (podcast_enabled/payments_state, verified live cycle 2418 to be present on every
// leaderboard entry, same shape as the homepage preload) — zero extra requests, same "count what
// the filter dropped" rule as discoverTypeSkipped above.
let discoverAttrSkipped = 0;
// cycle 812: same rule one branch over. When discovery yields nothing and discoverType is NOT the
// cause, the old remedy said "try a different category or raise maxPublicationsPerCategory" — both
// unreachable. Verified live (cycle 812): all 33 categories x all 3 leaderboardTiers return a full
// 25-publication page with more:true, so an empty `found` with no type-skips means the leaderboard
// REQUEST failed, not that the category is thin. Record the failure so the message can say "re-run".
const discoverFetchFailures = [];
// cycle 2348: the three trackers below exist because every discovery-path problem used to be
// reported ONLY through the two "nothing to do" branches, i.e. only when it took down the WHOLE
// run. A PARTIAL miss — one typo'd slug among several good ones, one category's leaderboard
// failing, or the time budget cutting the category walk short — left the run delivering real rows,
// charging in full, and saying nothing at all about the category the buyer never got.
// `unknownCategorySlugs` is distinct from the existing `unknownCategories` flag, which is true only
// when EVERY requested slug failed to resolve.
const unknownCategorySlugs = [];
// Set to the error message when substack.com/api/v1/categories itself could not be read, so the
// zero-row advice can say "re-run" instead of the misleading "use a valid slug".
let categoryListFailed = null;
// Categories that resolved fine but were never walked because timeBudgetOk() broke the loop.
let categoriesNotScanned = 0;
// Origins whose opt-in publication-info lookup was skipped (thin budget) or failed: those rows ship
// with every publicationXxx field null even though the buyer explicitly asked for them.
const pubInfoUnavailable = new Set();

// Shared by both zero-row paths below (leaderboardOnly and post scraping) so their advice can never
// drift apart, which is how the stale "raise maxPublicationsPerCategory" survived in one of them.
const noDiscoveryWhy = () => (discoverFetchFailures.length
  ? `the Substack leaderboard request failed, so no publications could be read (${discoverFetchFailures.join('; ')})`
    + ' — every Substack category normally returns publications, so this is a transient Substack-side'
    + ' or rate-limit failure: re-run the Actor. Changing discoverCategories, leaderboardTier or'
    + ' maxPublicationsPerCategory will not help'
  : `the "${leaderboardTier}" leaderboard returned no publications for ${discoverCategories.join(', ')}`
    + ' — try leaderboardTier="all", or a different category slug from substack.com/api/v1/categories'
    + ' (raising maxPublicationsPerCategory cannot help: the leaderboard was already read to its last page)');

// The PARTIAL-miss counterpart of noDiscoveryWhy(), shared by both delivering branches
// (leaderboardOnly and post scraping) for the same anti-drift reason. Each cause here is one a run
// can hit while still returning rows, so each must be listed independently rather than picked:
// a typo'd slug and a failed leaderboard are different problems with different remedies, and the
// buyer paid for both categories. `discoverTypeSkipped` is deliberately NOT here — it only moves
// when discoverType !== 'all', i.e. the buyer asked for that filtering, so reporting it on an
// otherwise healthy run would be noise, not a degraded result.
const partialDiscoveryNotes = () => {
  const notes = [];
  if (unknownCategorySlugs.length) {
    notes.push(
      `${unknownCategorySlugs.length} of the ${discoverCategories.length} discoverCategories you listed`
      + ` is not a Substack category and was skipped, so nothing from it is in this result`
      + ` (${unknownCategorySlugs.join(', ')}) — valid slugs come from substack.com/api/v1/categories`,
    );
  }
  if (discoverFetchFailures.length) {
    notes.push(
      `the leaderboard request failed for ${discoverFetchFailures.join('; ')}, so no publications were`
      + ' read from it — this is normally transient, re-run to pick that category up',
    );
  }
  if (categoriesNotScanned) {
    notes.push(
      `${categoriesNotScanned} of the ${discoverCategories.length} categories were never opened —`
      + ' the run ran out of time before reaching them; use fewer discoverCategories per run',
    );
  }
  return notes;
};

async function discoverPublications(cat) {
  const found = [];
  const entries = [];
  let skippedByType = 0;
  let skippedByAttr = 0;
  const pageSize = 25;
  for (let page = 0; found.length < maxPublicationsPerCategory && timeBudgetOk(); page += 1) {
    const url = `https://substack.com/api/v1/category/public/${cat.id}/${leaderboardTier}?page=${page}&limit=${pageSize}`;
    let body;
    try {
      body = await getJson(url);
    } catch (e) {
      log.warning(`Category "${cat.slug}" page ${page} failed: ${e.message}`);
      if (!found.length) discoverFetchFailures.push(`${cat.slug} page ${page}: ${e.message}`);
      break;
    }
    const pubs = body?.publications;
    if (!Array.isArray(pubs) || !pubs.length) break;
    pubs.forEach((p, i) => {
      const rank = page * pageSize + i + 1;
      if (discoverType !== 'all' && p.type && p.type !== discoverType) { skippedByType += 1; return; }
      if (requirePodcast && !(p.podcast_enabled ?? p.has_podcast)) { skippedByAttr += 1; return; }
      if (requirePaymentsEnabled && p.payments_state !== 'enabled') { skippedByAttr += 1; return; }
      const host = p.custom_domain || (p.subdomain ? `${p.subdomain}.substack.com` : null);
      if (!host) return;
      if (found.length >= maxPublicationsPerCategory) return;
      found.push({ origin: `https://${host}`, postSlug: null, pubName: p.name });
      entries.push({ rank, category: cat.slug, tier: leaderboardTier, origin: `https://${host}`, pub: p });
    });
    if (!body.more) break;
  }
  log.info(`Category "${cat.slug}" (${leaderboardTier}): discovered ${found.length} publication(s)${found.length ? ` — ${found.slice(0, 5).map((f) => f.pubName).join(', ')}${found.length > 5 ? ', …' : ''}` : ''}`);
  discoverTypeSkipped += skippedByType;
  if (skippedByType && !found.length) {
    log.warning(`Category "${cat.slug}" (${leaderboardTier}): every one of the ${skippedByType} publication(s) on the leaderboard was dropped by discoverType="${discoverType}" — Substack's category leaderboards are almost entirely "newsletter" publications, so discoverType="podcast" usually matches nothing outside the "podcast" category. Raising maxPublicationsPerCategory will not help (the whole leaderboard was already read); set discoverType="all" instead, and use contentType="podcast" if what you want is podcast *episodes* rather than podcast-type publications.`);
  } else if (skippedByType) {
    log.info(`Category "${cat.slug}": ${skippedByType} publication(s) skipped by discoverType="${discoverType}".`);
  }
  discoverAttrSkipped += skippedByAttr;
  if (skippedByAttr && !found.length) {
    log.warning(`Category "${cat.slug}" (${leaderboardTier}): every one of the ${skippedByAttr} publication(s) on the leaderboard was dropped by ${attrFilterLabel()} — try leaderboardTier="paid" (for requirePaymentsEnabled) or the dedicated "podcast" category (for requirePodcast) instead, or turn the filter off and check the publicationHasPodcast/publicationPaymentsEnabled fields on the results yourself.`);
  } else if (skippedByAttr) {
    log.info(`Category "${cat.slug}": ${skippedByAttr} publication(s) skipped by ${attrFilterLabel()}.`);
  }
  return { found, entries };
}

function mapLeaderboardEntry(e) {
  return {
    type: 'leaderboard',
    rank: e.rank,
    category: e.category,
    leaderboardTier: e.tier,
    name: e.pub.name ?? null,
    publicationUrl: e.origin,
    handle: e.pub.subdomain ?? null,
    customDomain: e.pub.custom_domain ?? null,
    ...mapPublicationInfo(e.pub),
  };
}

// publicationUrls carries a schema default (the sample "astralcodexten" publication) so Apify's
// automated {} Store test still returns rows (PLAYBOOK step 4c). The platform auto-fills that
// same default array whenever a caller sets discoverCategories OR postUrls and never touches
// publicationUrls at all — which used to mean the sample publication got silently scraped and
// billed alongside the caller's actual request. Drop it whenever either alternate seed is used;
// a caller who really wants both can just list the sample publication in publicationUrls
// explicitly (any form other than the exact default string).
const DEFAULT_PUBLICATION_URLS = ['https://astralcodexten.substack.com'];
const rawPublicationUrls = input.publicationUrls ?? [];
const rawPostUrls = input.postUrls ?? [];
const publicationUrlsIsUntouchedDefault = (discoverCategories.length > 0 || rawPostUrls.length > 0)
  && rawPublicationUrls.length === DEFAULT_PUBLICATION_URLS.length
  && rawPublicationUrls.every((u, i) => String(u) === DEFAULT_PUBLICATION_URLS[i]);
if (publicationUrlsIsUntouchedDefault) {
  log.info(`${discoverCategories.length > 0 ? 'discoverCategories' : 'postUrls'} is set and publicationUrls was left at its default sample publication — scraping only the requested content, not the sample.`);
}
const effectivePublicationUrls = publicationUrlsIsUntouchedDefault ? [] : rawPublicationUrls;

const publicationTargets = [];
const postTargets = [];
for (const raw of effectivePublicationUrls) {
  const t = parseTarget(raw);
  if (t) (t.postSlug ? postTargets : publicationTargets).push(t);
}
for (const raw of rawPostUrls) {
  const t = parseTarget(raw);
  if (t?.postSlug) postTargets.push(t);
  else if (t) publicationTargets.push(t);
}
let unknownCategories = false;
let categoriesScanned = 0;
const leaderboardEntries = [];
if (discoverCategories.length) {
  // Verified live cycle 839 across 3 categories at every page depth (culture/technology/humor,
  // 15+ pages each): category/public/<id>/free is NOT a real Substack leaderboard tier. It
  // returns the byte-identical publication list, in the same order, as /all — never a free-only
  // ranking. /paid genuinely returns a different, separately-ranked list, so only "all"/"paid"
  // are real. There is no cheap client-side substitute (a publication's payments_state does not
  // reliably predict membership in the /paid list, so it cannot be used to reconstruct a true
  // free-only set).
  if (leaderboardTier === 'free') {
    log.warning(
      'leaderboardTier="free" is not a real Substack leaderboard filter — verified live, it returns'
      + ' the exact same list as "all" (which mixes free and paid-tier publications), never a'
      + ' free-only ranking. Use leaderboardTier="paid" to find monetized newsletters instead.',
    );
  }
  const cats = await resolveCategoryIds(discoverCategories);
  unknownCategories = cats.length === 0;
  for (const [i, cat] of cats.entries()) {
    // A break here used to be invisible: the leaderboardOnly message below counted the categories
    // the buyer ASKED for, not the ones actually walked, so a budget-truncated run claimed full
    // coverage of categories it never opened.
    if (!timeBudgetOk()) { categoriesNotScanned = cats.length - i; break; }
    const { found, entries } = await discoverPublications(cat);
    publicationTargets.push(...found);
    leaderboardEntries.push(...entries);
  }
  categoriesScanned = cats.length - categoriesNotScanned;
}

if (leaderboardOnly) {
  // Leaderboard rows are publication summaries, not posts — audience/contentType/date/engagement
  // filters only ever run inside the post-scraping path below this block, which leaderboardOnly
  // skips entirely (Actor.exit() a few lines down). Without this warning a buyer combining e.g.
  // minReactionCount with leaderboardOnly would see it silently do nothing.
  if (filtersActive) {
    log.warning('leaderboardOnly is on — audienceFilter/contentType/publishedAfter/publishedBefore/minReactionCount/minCommentCount/minRestackCount/minWordCount/maxWordCount only apply to post scraping and are ignored for leaderboard rows.');
  }
  if (!leaderboardEntries.length) {
    const why = categoryListFailed
      ? `Substack's category list could not be read (${categoryListFailed}), so no discoverCategories slug could be resolved — this is transient, re-run the Actor (the slugs you passed may be perfectly valid)`
      : unknownCategories
        ? 'none of the discoverCategories matched a Substack category — use a slug from substack.com/api/v1/categories (e.g. technology, business, finance)'
          : discoverTypeSkipped
            ? `discoverType="${discoverType}" dropped every publication on the leaderboard(s) (${discoverTypeSkipped} in total) — Substack's category leaderboards are almost entirely "newsletter" publications, so set discoverType="all" (raising maxPublicationsPerCategory will not help)`
            : discoverAttrSkipped
              ? `${attrFilterLabel()} dropped every publication on the leaderboard(s) (${discoverAttrSkipped} in total) — turn the filter off and check publicationHasPodcast/publicationPaymentsEnabled on the results if you want to see what was excluded`
              : discoverCategories.length
                ? noDiscoveryWhy()
                : 'leaderboardOnly requires discoverCategories — publicationUrls/postUrls are not used in this mode';
    log.warning(`Nothing to do — ${why}.`);
    await Actor.setStatusMessage(`No items returned — ${why}.`);
  } else {
    let rowsLeft = false;
    for (const e of leaderboardEntries) {
      if (!(await pushResult(mapLeaderboardEntry(e), 'leaderboard-row'))) {
        // pushResult() returns false on the maxResults cap, on eventChargeLimitReached, and on a
        // charge that could not be made at all — all three truncate the leaderboard silently.
        rowsLeft = pushed < leaderboardEntries.length;
        break;
      }
    }
    // Count what was actually walked, not what was asked for: a typo'd slug, a failed leaderboard
    // request or a time-budget break all leave categoriesScanned below discoverCategories.length.
    const notes = partialDiscoveryNotes();
    if (rowsLeft) {
      notes.push(
        pushed >= maxResults
          ? `stopped at your maxResults cap (${maxResults}) — ${leaderboardEntries.length - pushed} more leaderboard row(s) were discovered but not returned; raise maxResults to get them`
          : `stopped early: the run could not charge for further rows (pay-per-event budget reached) — ${leaderboardEntries.length - pushed} discovered row(s) were not returned`,
      );
    }
    await Actor.setStatusMessage(
      `Pushed ${pushed} leaderboard row(s) across ${categoriesScanned} categor${categoriesScanned === 1 ? 'y' : 'ies'}.`
      + (notes.length ? ` NOTE — this result is incomplete: ${notes.join('; ')}.` : ''),
    );
  }
  await Actor.exit();
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
// Publications whose <handle>.substack.com redirects to a substack.com/@handle PROFILE page
// instead of the real archive (verified live, cycle 1969: lennysnewsletter.substack.com -> 302 ->
// https://substack.com/@lennysnewsletter, which returns HTML, not the archive JSON). The
// followRedirect:true comment on getJson assumed every redirect lands on the custom domain; this
// is a second redirect shape where it lands on a dead end instead. Tracked separately from
// `errored` because the fix (pass the exact custom domain URL, not the bare handle) is different
// from a generic "check the URL is correct."
const profileRedirected = [];

if (!publicationTargets.length && !postTargets.length) {
  const why = categoryListFailed
    ? `Substack's category list could not be read (${categoryListFailed}), so no discoverCategories slug could be resolved — this is transient, re-run the Actor (the slugs you passed may be perfectly valid)`
    : unknownCategories
      ? 'none of the discoverCategories matched a Substack category — use a slug from substack.com/api/v1/categories (e.g. technology, business, finance)'
      : discoverTypeSkipped
        ? `discoverType="${discoverType}" dropped every publication on the leaderboard(s) (${discoverTypeSkipped} in total) — Substack's category leaderboards are almost entirely "newsletter" publications, so set discoverType="all" (raising maxPublicationsPerCategory will not help); use contentType="podcast" if you want podcast episodes rather than podcast-type publications`
        : discoverAttrSkipped
          ? `${attrFilterLabel()} dropped every publication on the leaderboard(s) (${discoverAttrSkipped} in total) — turn the filter off and check publicationHasPodcast/publicationPaymentsEnabled on the results if you want to see what was excluded`
          : discoverCategories.length
            ? noDiscoveryWhy()
            : 'no publicationUrls, postUrls or discoverCategories were provided';
  log.warning(`Nothing to do — ${why}.`);
  await Actor.setStatusMessage(`No items returned — ${why}.`);
} else {
  // Targets the loops below never even attempted because keepGoing went false (maxResults cap or
  // the pay-per-event budget). Previously invisible: those publications land in none of
  // errored/empty/filtered, so a 10-publication run truncated at publication 3 reported only on
  // the 3 it reached and looked complete.
  let unreachedTargets = 0;
  for (const [i, t] of postTargets.entries()) {
    if (!keepGoing) { unreachedTargets += postTargets.length - i; break; }
    const label = t.origin && t.postSlug ? `${t.origin}/p/${t.postSlug}` : t.origin;
    const detail = await fetchDetail(t.origin, t.postSlug);
    if (!detail) { errored.push(label); continue; }
    const pushedBefore = pushed;
    // Same accounting as the guard above — this break skips the remaining targets too, and
    // bypasses the guard that would otherwise have counted them.
    if (!(await handlePost(detail, t.origin, detail))) { unreachedTargets += postTargets.length - i - 1; break; }
    if (pushed === pushedBefore) filtered.push(label);
  }
  for (const [i, t] of publicationTargets.entries()) {
    if (!keepGoing) { unreachedTargets += publicationTargets.length - i; break; }
    const result = await scrapePublication(t.origin);
    // profileRedirected is more specific than a generic error — don't also report it there,
    // same dedup rule as depthCapped vs filtered (avoid two causes giving different advice).
    if (result === 'error' && !profileRedirected.includes(t.origin)) errored.push(t.origin);
    else if (result === 'empty') empty.push(t.origin);
    else if (result === 'filtered') filtered.push(t.origin);
  }

  const timeBudgetNote = timeBudgetExceeded
    ? 'stopped early, approaching the run timeout — narrow publicationUrls/discoverCategories or lower maxPostsPerPublication/maxPublicationsPerCategory to get a complete run'
    : null;
  // keepGoing also goes false on a timeout, but that already has its own note above — only report
  // the cap/charge causes here so a timed-out run isn't blamed on maxResults it never reached.
  const truncationNote = (keepGoing || timeBudgetExceeded)
    ? null
    : pushed >= maxResults
      ? `stopped at your maxResults cap (${maxResults})${unreachedTargets ? `, leaving ${unreachedTargets} of the publication(s)/post(s) you asked for completely unscraped` : ''} — raise maxResults for a complete result`
      : `stopped early: the run could not charge for further results (pay-per-event budget reached)${unreachedTargets ? `, leaving ${unreachedTargets} of the publication(s)/post(s) you asked for completely unscraped` : ''} — raise the Actor's spend limit for a complete result`;
  // Discovery problems that left the run still delivering rows (partial, not total, failures).
  const discoveryNotes = partialDiscoveryNotes();
  if (pushed === 0 && (publicationTargets.length || postTargets.length)) {
    // These causes are NOT mutually exclusive — e.g. the time budget can run out partway through
    // a publication whose posts seen so far were all filtered out, or one target can error while
    // another comes back empty. Collect every applicable cause instead of picking just one, or a
    // real cause silently goes unmentioned (verified live: an impossible minWordCount plus a tight
    // ACTOR_TIMEOUT_AT produced ONLY the time-budget wording, hiding that all 473 posts actually
    // scanned were filter-excluded — a buyer narrowing publicationUrls per that advice alone would
    // still see 0 rows, since the real fix is widening the filter).
    const causes = [];
    if (timeBudgetNote) causes.push(timeBudgetNote);
    if (truncationNote) causes.push(truncationNote);
    causes.push(...discoveryNotes);
    if (profileRedirected.length) causes.push(`${profileRedirected.join(', ')} redirected to a Substack profile page instead of the archive — pass the exact custom domain or "<handle>.substack.com" homepage URL instead of the bare handle`);
    if (errored.length) causes.push(`the request failed for: ${errored.join(', ')} (see log for the error — check the publication/post URL is correct)`);
    if (filtered.length) causes.push(`every post matching ${filtered.join(', ')} was excluded by audienceFilter/contentType/publishedAfter/publishedBefore/min-max filters — try widening those filters`);
    if (depthCapped.length) causes.push(`hit maxPostsPerPublication (${maxPostsPerPublication}) for: ${depthCapped.join(', ')} before finding a match — the cap counts posts scanned before filters, so raise it to search deeper`);
    if (empty.length) causes.push(`no posts were found for: ${empty.join(', ')} — the publication may be empty, private, or the URL/handle is wrong`);
    await Actor.setStatusMessage(`No items returned — ${causes.join('; ')}.`);
  } else if (errored.length || empty.length || filtered.length || depthCapped.length || profileRedirected.length || timeBudgetNote || postsWithCommentsWithheld || truncationNote || discoveryNotes.length || pubInfoUnavailable.size) {
    const notes = [];
    if (timeBudgetNote) notes.push(timeBudgetNote);
    if (truncationNote) notes.push(truncationNote);
    notes.push(...discoveryNotes);
    if (pubInfoUnavailable.size) {
      notes.push(
        `the publication profile lookup you asked for (includePublicationInfo) could not be read for`
        + ` ${[...pubInfoUnavailable].join(', ')}, so every publicationXxx field is null on those rows`
        + ' (the post content itself is unaffected) — re-run, or set includePublicationInfo:false if you do not need it',
      );
    }
    if (postsWithCommentsWithheld) {
      notes.push(
        `Substack withheld the comment section on ${postsWithCommentsWithheld} subscriber-only post(s)`
        + ' (flagged commentsWithheld:true — set audienceFilter:"free" to scrape only posts whose comments are public)',
      );
    }
    if (profileRedirected.length) notes.push(`${profileRedirected.join(', ')} redirected to a Substack profile page instead of the archive — use the exact custom domain or "<handle>.substack.com" homepage URL instead of the bare handle`);
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
