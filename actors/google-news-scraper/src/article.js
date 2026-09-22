import * as cheerio from 'cheerio';

// ---- Full article extraction (opt-in) ------------------------------------
// Publishers serve very different HTML to different clients: some 403 a plain UA, some hide the
// body behind a consent interstitial for EU-looking requests, some only ship the text to a
// browser-ish fingerprint. Same failure class as Apple's review RSS (see app-store-reviews-scraper),
// so use the same treatment: retry the page under other fingerprints, and remember per publisher
// which one worked so the steady state stays at one request per article.
const PAGE_VARIANTS = [
  {},
  { headerGeneratorOptions: { browsers: ['firefox'], devices: ['desktop'], operatingSystems: ['windows'] } },
  { headers: { 'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' } },
];
const ARTICLE_TYPES = /(news)?article|blogposting|report(age)?|liveblog/i;
const clean = (s) => String(s ?? '').replace(/\s*\n\s*/g, '\n').replace(/[ \t ]+/g, ' ').replace(/\n{3,}/g, '\n\n').trim();
const firstName = (v) => {
  const one = Array.isArray(v) ? v[0] : v;
  if (!one) return null;
  return clean(typeof one === 'object' ? one.name : one) || null;
};
const firstUrl = (v) => {
  const one = Array.isArray(v) ? v[0] : v;
  if (!one) return null;
  return (typeof one === 'object' ? one.url || one.contentUrl : one) || null;
};

// Walk every JSON-LD block (including @graph containers) and return the first Article-ish node.
function findArticleLd($) {
  const nodes = [];
  $('script[type="application/ld+json"]').each((_, el) => {
    try {
      const raw = JSON.parse($(el).contents().text().trim());
      for (const n of Array.isArray(raw) ? raw : [raw]) {
        if (!n || typeof n !== 'object') continue;
        nodes.push(n, ...(Array.isArray(n['@graph']) ? n['@graph'] : []));
      }
    } catch { /* publishers ship broken JSON-LD all the time; just skip the block */ }
  });
  return nodes.find((n) => {
    const t = n['@type'];
    return (Array.isArray(t) ? t : [t]).some((x) => typeof x === 'string' && ARTICLE_TYPES.test(x));
  }) || null;
}

const MIN_BODY_CHARS = 300; // shorter than this is a teaser/consent wall, not an article

// Did we get the WHOLE article, or a paywall teaser that merely looks like one?
//
// A teaser is the dangerous failure: it arrives as real <p> paragraphs, clears every length
// threshold, and reports articleFetchStatus:"ok" with no hint that the rest is missing.
//
// The naive check -- "JSON-LD says isAccessibleForFree:false, therefore incomplete" -- is WRONG,
// and we measured it: theatlantic.com declares isAccessibleForFree:false on every article yet
// served us the full 3,479-word body. Metered paywalls gate the Nth read, not the first, so the
// flag describes the publisher's intent, never what this response actually contained.
//
// So we never trust the flag as a verdict; we use it as a MAP. Google's paywall spec makes the
// publisher name the gated region in `hasPart[].cssSelector`, so we can go look at that exact
// region in the HTML we were served and see whether the text is in it. That turns an assumption
// into an observation. Where no observation is possible we return null, never false -- a guessed
// "incomplete" is as bad for a buyer as a silent teaser.
// Run this on the UNTOUCHED document, before bodyFromHtml() strips noise elements out of it --
// one of those strip rules could otherwise remove the very region we are trying to inspect.
function probeGatedRegion($, ld) {
  const parts = (Array.isArray(ld.hasPart) ? ld.hasPart : [ld.hasPart]).filter((p) => p && typeof p === 'object');
  for (const part of parts) {
    const partGated = part.isAccessibleForFree === false || String(part.isAccessibleForFree).toLowerCase() === 'false';
    if (!partGated || !part.cssSelector) continue;
    let scope;
    try { scope = $(String(part.cssSelector)); } catch { continue; } // publishers ship selectors cheerio can't parse
    if (!scope.length) return { served: false, reason: 'paywalled-section-missing' };
    const text = clean(scope.find('p').map((_, p) => clean($(p).text())).get().filter((t) => t.length > 40).join('\n\n'));
    if (text.length < MIN_BODY_CHARS) return { served: false, reason: 'paywalled-section-empty' };
    return { served: true, reason: null }; // the gated region was served to us in full
  }
  return null; // publisher named no inspectable gated region
}

// A gated region that came back empty is NOT on its own proof of a teaser, and we measured this
// too: scmp.com points `cssSelector` at `.piano-metering__paywall-container`, the client-side
// paywall OVERLAY, which is correctly empty on a free read. Treating "gated region empty" as
// "article truncated" flagged two complete 849- and 1,123-word SCMP articles as incomplete.
// So an empty gated region only downgrades to `false` when a SECOND, independent observation
// agrees that what we hold is teaser-sized. One observation short of that, we say `null`.
const TEASER_MAX_WORDS = 220;

function assessCompleteness(probe, ld, deliveredWords) {
  const n = Number(ld.wordCount);
  const declaredWordCount = Number.isFinite(n) && n > 0 ? n : null;
  const free = ld.isAccessibleForFree;
  const isFalse = free === false || String(free).toLowerCase() === 'false';
  const isTrue = free === true || String(free).toLowerCase() === 'true';

  // Publisher declares its own length and we fell well short of it: incomplete on our own numbers,
  // independent of any paywall claim. Both counts ride on the row so a buyer can re-judge the ratio.
  if (declaredWordCount && deliveredWords < declaredWordCount * 0.6) {
    return { declaredWordCount, complete: false, reason: 'short-vs-declared-wordcount' };
  }
  if (probe?.served) return { declaredWordCount, complete: true, reason: null };
  if (probe && deliveredWords <= TEASER_MAX_WORDS) {
    return { declaredWordCount, complete: false, reason: probe.reason };
  }
  // Gated, but nothing we can check came back conclusive: either the publisher named no region for
  // us to inspect, or the region was empty while the text we hold is full-article-sized. We know it
  // is paywalled and we do NOT know whether this response was truncated. Say exactly that.
  if (probe || isFalse) return { declaredWordCount, complete: null, reason: 'paywall-declared-unverifiable' };
  if (isTrue || declaredWordCount) return { declaredWordCount, complete: true, reason: null };
  return { declaredWordCount, complete: null, reason: null }; // no completeness signal on the page
}

// Fallback when JSON-LD has no articleBody: pull the paragraphs out of the article container.
function bodyFromHtml($) {
  // Most specific container first: a publisher-specific body wrapper carries less caption/bio
  // noise than the whole <article>, which is itself tighter than <main>.
  const SCOPES = ['[itemprop="articleBody"]', '[class*="article-body"]', '[class*="story-body"]', '[data-component="text-block"]', 'article', 'main', 'body'];
  $('script, style, nav, aside, footer, header, form, figure, figcaption, .ad, [class*="newsletter"], [class*="related"]').remove();
  // Widen until one actually yields text: a publisher can have an empty <article> wrapper with the
  // real paragraphs outside it, so stopping at the first scope that *matches* loses the body.
  for (const sel of SCOPES) {
    const scope = $(sel).first();
    if (!scope.length) continue;
    const paras = scope.find('p').map((_, p) => clean($(p).text())).get().filter((t) => t.length > 40);
    const text = clean(paras.join('\n\n'));
    if (text.length >= MIN_BODY_CHARS) return text;
  }
  return null;
}

export function makeArticleFetcher({ http, bodyMaxChars, log }) {
  const hostVariant = new Map(); // publisher hostname -> index of the fingerprint that last worked
  return async function fetchArticle(url) {
    let host; try { host = new URL(url).hostname; } catch { return { articleFetchStatus: 'error' }; }
    const preferred = hostVariant.get(host) ?? 0;
    const order = [preferred, ...PAGE_VARIANTS.keys()].filter((v, i, a) => a.indexOf(v) === i);
    let status = 'no-body';
    for (const i of order) {
      let $;
      try {
        const res = await http(url, { ...PAGE_VARIANTS[i], timeout: { request: 25000 }, retry: { limit: 1 }, throwHttpErrors: false });
        if (res.statusCode >= 400) { status = res.statusCode === 403 || res.statusCode === 401 ? 'blocked' : 'error'; continue; }
        $ = cheerio.load(res.body);
      } catch (e) { log.debug(`article fetch failed (${url}): ${e.message}`); status = 'error'; continue; }
      const ld = findArticleLd($) ?? {};
      const gatedProbe = probeGatedRegion($, ld); // before bodyFromHtml() mutates the document
      const ldBody = clean(ld.articleBody);
      const body = ldBody.length >= MIN_BODY_CHARS ? ldBody : bodyFromHtml($) ?? (ldBody || null);
      if (!body) continue; // this fingerprint got a page without the text — try the next one
      hostVariant.set(host, i);
      const words = body.split(/\s+/).filter(Boolean).length;
      const { declaredWordCount, complete, reason } = assessCompleteness(gatedProbe, ld, words);
      const kw = ld.keywords ?? $('meta[name="news_keywords"]').attr('content') ?? $('meta[name="keywords"]').attr('content');
      return {
        articleBody: body.slice(0, bodyMaxChars),
        articleBodyTruncated: body.length > bodyMaxChars,
        articleWordCount: words,
        articleDeclaredWordCount: declaredWordCount,
        articleBodyComplete: complete,
        articleBodyIncompleteReason: reason,
        articleBodySource: ldBody.length >= MIN_BODY_CHARS ? 'jsonld' : 'html',
        articleAuthor: firstName(ld.author) || clean($('meta[name="author"]').attr('content')) || null,
        articleImage: firstUrl(ld.image) ?? $('meta[property="og:image"]').attr('content') ?? null,
        articleKeywords: (Array.isArray(kw) ? kw : String(kw ?? '').split(',')).map((k) => clean(k)).filter(Boolean),
        articleSection: firstName(ld.articleSection) ?? null,
        articleDescription: clean(ld.description) || clean($('meta[property="og:description"]').attr('content')) || null,
        articlePublishedAt: ld.datePublished ?? null,
        articleModifiedAt: ld.dateModified ?? null,
        articleFetchStatus: 'ok',
      };
    }
    return { articleFetchStatus: status };
  }
}
