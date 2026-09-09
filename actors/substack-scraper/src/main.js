// Substack Scraper — HTTP-only, pay-per-event.
// Uses Substack's public JSON endpoints (no login, no headless browser):
//   GET <pub>/api/v1/archive?sort=new&offset=&limit=      -> post list (metadata only, no body)
//   GET <pub>/api/v1/archive?sort=new&search=<q>&...      -> in-publication search
//   GET <pub>/api/v1/posts/<slug>                          -> single post incl. body_html
//   GET <pub>/api/v1/post/<id>/comments?all_comments=true  -> comment tree
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';

await Actor.init();
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

const cm = Actor.getChargingManager();
const isPPE = cm.getPricingInfo().isPayPerEvent;
let pushed = 0;

async function pushResult(item) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
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

let keepGoing = true;

async function fetchDetail(origin, slug) {
  try {
    return await getJson(`${origin}/api/v1/posts/${encodeURIComponent(slug)}`);
  } catch (e) {
    log.warning(`Could not fetch full post ${origin}/p/${slug}: ${e.message}`);
    return null;
  }
}

async function handlePost(post, origin, preloadedDetail = null) {
  if (!matchesAudience(post) || !matchesDate(post)) return true;
  const needDetail = includeBodyText || includeBodyHtml;
  const detail = preloadedDetail ?? (needDetail && post.slug ? await fetchDetail(origin, post.slug) : null);
  keepGoing = await pushResult(mapPost(post, origin, detail));
  if (!keepGoing) return false;

  if (includeComments && (post.comment_count ?? 0) > 0) {
    try {
      const body = await getJson(`${origin}/api/v1/post/${post.id}/comments?token=&all_comments=true&sort=best_first`);
      const flat = flattenComments(body.comments).slice(0, maxCommentsPerPost);
      for (const c of flat) {
        keepGoing = await pushResult(mapComment(c, post, origin));
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
  let requestFailed = false;
  while (keepGoing && seen < maxPostsPerPublication) {
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
  return pushed > pushedBefore ? 'ok' : 'filtered';
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

const errored = [];
const empty = [];
const filtered = [];

if (!publicationTargets.length && !postTargets.length) {
  log.warning('No publicationUrls or postUrls provided — nothing to do.');
  await Actor.setStatusMessage('No items returned — no publicationUrls or postUrls were provided.');
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

  if (pushed === 0 && (publicationTargets.length || postTargets.length)) {
    const why = errored.length
      ? `the request failed for: ${errored.join(', ')} (see log for the error — check the publication/post URL is correct)`
      : filtered.length && !empty.length
        ? `every post matching ${filtered.join(', ')} was excluded by audienceFilter/publishedAfter/publishedBefore — try widening those filters`
        : `no posts were found for: ${empty.concat(filtered).join(', ')} — the publication may be empty, private, or the URL/handle is wrong`;
    await Actor.setStatusMessage(`No items returned — ${why}.`);
  } else if (errored.length || empty.length || filtered.length) {
    const notes = [];
    if (errored.length) notes.push(`request failed for ${errored.join(', ')}`);
    if (empty.length) notes.push(`no posts found for ${empty.join(', ')}`);
    if (filtered.length) notes.push(`filters excluded everything from ${filtered.join(', ')}`);
    await Actor.setStatusMessage(`Pushed ${pushed} items. ${notes.join('; ')}.`);
  }
}

log.info(`Done. Pushed ${pushed} items.`);
await Actor.exit();
