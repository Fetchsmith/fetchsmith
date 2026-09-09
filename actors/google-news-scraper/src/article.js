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
    if (text.length >= 300) return text; // shorter than this is a teaser/consent wall, not an article
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
      const ldBody = clean(ld.articleBody);
      const body = ldBody.length >= 300 ? ldBody : bodyFromHtml($) ?? (ldBody || null);
      if (!body) continue; // this fingerprint got a page without the text — try the next one
      hostVariant.set(host, i);
      const kw = ld.keywords ?? $('meta[name="news_keywords"]').attr('content') ?? $('meta[name="keywords"]').attr('content');
      return {
        articleBody: body.slice(0, bodyMaxChars),
        articleBodyTruncated: body.length > bodyMaxChars,
        articleWordCount: body.split(/\s+/).filter(Boolean).length,
        articleBodySource: ldBody.length >= 300 ? 'jsonld' : 'html',
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
