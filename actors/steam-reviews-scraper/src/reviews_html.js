// Steam community HTML review source — the replacement for the retired
// `store.steampowered.com/appreviews/<appid>?json=1` JSON API, which Valve shut off on
// 2026-10-22 (that URL now answers 302 -> store homepage with an empty body; re-verified
// 2026-10-23). Everything in here was characterised against live pages, not inferred; the
// per-finding evidence lives in tasks/queue.md under the steam P0 item.
//
// Design rule: `parseReviewsPage` emits review objects in the SAME SHAPE as the dead JSON
// API's `reviews[]` entries (recommendationid / voted_up / timestamp_created / author.* in
// minutes / ...). That keeps `reviewRow()` in main.js working unchanged and confines the
// outage fix to the fetch+parse layer instead of rippling through row building, filtering,
// watch-mode keying and the PPE charge path.
import { load } from 'cheerio';

// Steam's own rating filter is a PATH SEGMENT, not a query param: the page's
// filterrating_option_0/1/2 handlers link to /reviews/, /positivereviews/ and
// /negativereviews/. Confirmed from the rendered filter menu on app 1145360.
const REVIEW_TYPE_PATH = { all: 'reviews', positive: 'positivereviews', negative: 'negativereviews' };

// This Actor's `sortBy` values come from the dead API's vocabulary; the community page uses
// its own `browsefilter` names. Values confirmed present in the page's filter menu.
const SORT_TO_BROWSEFILTER = { recent: 'mostrecent', updated: 'recentlyupdated', all: 'toprated', funny: 'funny' };

export const browseFilterFor = (sortBy) => SORT_TO_BROWSEFILTER[sortBy] ?? 'mostrecent';
export const reviewTypePath = (reviewType) => REVIEW_TYPE_PATH[reviewType] ?? 'reviews';

// `?p=N` on the /reviews/ page is a NO-OP on content (verified live: p=1..5 all served the
// same 10 cards). Real paging is the "Show More" GET form -> /app/<id>/homecontent/ carrying
// a `userreviewscursor`. Only the first page comes from this URL; every later page comes from
// homeContentUrl() below.
export function reviewsPageUrl(appId, { reviewType = 'all', sortBy = 'recent', language = 'all' } = {}) {
  const p = new URLSearchParams({ browsefilter: browseFilterFor(sortBy), filterLanguage: language, l: 'english' });
  return `https://steamcommunity.com/app/${appId}/${reviewTypePath(reviewType)}/?${p.toString()}`;
}

// The next page is requested by REPLAYING the Show-More form's own hidden fields verbatim
// (minus the other tabs' page counters) rather than by hand-picking the ones we think matter.
// Steam's form also carries `searchText`, `maxInappropriateScore` and `forceanon`, and it
// gained/changed fields between the initial page and the AJAX responses — replaying whatever
// it sends is what keeps this working when that set shifts again.
//
// `appHubSubSection=10` is NOT optional: without it, homecontent serves a mixed feed from
// every app-hub tab (measured live on app 1145360: 53 cards, only 3 of them reviews) instead
// of the reviews tab. The form always includes it, so replaying the form gets this right.
export function homeContentUrl(appId, next) {
  const p = new URLSearchParams(next.fields);
  return `https://steamcommunity.com/app/${appId}/homecontent/?${p.toString()}`;
}

const STEAMID64_BASE = 76561197960265728n;
// Every author block carries data-miniprofile="<32-bit accountid>", and
// steamid64 = accountid + 76561197960265728. Verified against the four cards on app
// 1145360 page 1 that expose a /profiles/<steamid64>/ URL directly (e.g. miniprofile
// 220218906 -> 76561198180484634). This removes the whole vanity-URL resolution problem:
// the 6-of-10 cards that link to /id/<vanity>/ still yield an exact, stable steamid64 with
// no extra request and no Steam Web API key.
export const steamIdFromMiniprofile = (mini) => {
  const n = Number(mini);
  return Number.isInteger(n) && n > 0 ? String(BigInt(n) + STEAMID64_BASE) : null;
};

const MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
// Two DIFFERENT word orders exist and both must be handled: the initial /reviews/ or
// /positivereviews/ page renders "Posted: 23 October" / "Posted: 24 August, 2020"
// (day-then-month), but the "Show More" homecontent AJAX response — i.e. every page after
// the first — renders the SAME dates as "Posted: October 22" / "Posted: December 20, 2023"
// (month-then-day). Found live while testing page 2+ of a chain: the day-then-month-only
// regex silently matched nothing past page 1, nulling timestamp_created for every row
// beyond the first page (which also breaks the reviewsAfter/reviewsBefore early-stop, since
// it compares against that field). Day resolution only either way — the dead API gave exact
// unix timestamps, so this is a real precision loss that the README has to state.
export function parsePostedDate(text, now = new Date()) {
  const m = /Posted:\s*(?:(\d{1,2})\s+([A-Za-z]+)|([A-Za-z]+)\s+(\d{1,2}))(?:,\s*(\d{4}))?/.exec(text || '');
  if (!m) return null;
  const day = Number(m[1] ?? m[4]);
  const month = MONTHS.indexOf((m[2] ?? m[3]).toLowerCase());
  if (month < 0 || !(day >= 1 && day <= 31)) return null;
  let year = m[5] ? Number(m[5]) : now.getUTCFullYear();
  // Year-omitted means "this year", but a run on 1 Jan can legitimately see "31 December"
  // from days earlier; without this the row would be dated ~1 year into the future.
  if (!m[5]) {
    const asThisYear = Date.UTC(year, month, day);
    if (asThisYear > now.getTime() + 86400000) year -= 1;
  }
  const t = Date.UTC(year, month, day);
  return Number.isFinite(t) ? Math.floor(t / 1000) : null;
}

// "2,205 people found this review helpful" / "38 people found this review funny" / the
// zero case "No one has rated this review as helpful yet" (no funny line at all when zero).
// All three phrasings seen live. Thousands separators are present, hence the comma strip.
const countFromPhrase = (text, word) => {
  const m = new RegExp(`([\\d,]+)\\s+(?:person|people)\\s+found this review ${word}`, 'i').exec(text || '');
  return m ? Number(m[1].replace(/,/g, '')) : 0;
};

const hoursFromText = (text) => {
  const m = /([\d,.]+)\s*hrs on record/i.exec(text || '');
  if (!m) return null;
  const h = Number(m[1].replace(/,/g, ''));
  return Number.isFinite(h) ? h : null;
};

/**
 * Parse one /reviews/ or /homecontent/ response.
 * @returns {{reviews: object[], next: {cursor:string,offset:number,p:number,numPerPage:number}|null,
 *            cardCount: number, idCount: number}}
 */
export function parseReviewsPage(html, appId, now = new Date()) {
  const $ = load(html);

  // The real recommendationid — the SAME id space as the dead JSON API, so existing
  // watch-mode baselines keyed on it stay valid across this fix. It is not on the card;
  // it only appears in the page's trailing
  // RequestCurrentUserRecommendationVotes(["id",...]) call, ordered to match the cards.
  // That pairing is verified, not assumed: card 1's author permalink
  // (steamcommunity.com/id/Dodest/recommended/1145360/) contains 238359551, which is
  // element 0 of that array.
  let ids = [];
  const idm = /RequestCurrentUserRecommendationVotes\(\s*\[([^\]]*)\]\s*\)/.exec(html);
  if (idm) ids = [...idm[1].matchAll(/"(\d+)"/g)].map((m) => m[1]);

  const cards = $('div.apphub_Card').toArray();
  const reviews = [];
  // A card/id length mismatch means the pairing assumption broke (Steam markup change).
  // Rows are still emitted, but with recommendationid null — main.js already refuses to
  // deliver an id-less row in watch mode (unidentifiedSkipped) rather than re-charging for
  // it every run, which is the correct conservative failure.
  const paired = ids.length === cards.length;

  cards.forEach((el, i) => {
    const card = $(el);
    const textBlock = card.find('.apphub_CardTextContent').first();
    const posted = textBlock.find('.date_posted').first().text();
    const earlyAccess = textBlock.find('.early_access_review').length > 0;
    // The review body is the card text with the date line and the Early Access badge
    // removed — both are children of the same div as the prose.
    const body = textBlock.clone();
    body.find('.date_posted, .early_access_review').remove();
    const review = body.text().replace(/ /g, ' ').trim();

    const helpfulText = card.find('.found_helpful').first().text();
    // Icon filename, not the "Recommended"/"Not Recommended" label: the icon is
    // language-independent, so this keeps working if Steam ever ignores l=english.
    const thumb = card.find('.thumb img').first().attr('src') || '';
    const voted = /thumbsUp/i.test(thumb) ? true : (/thumbsDown/i.test(thumb) ? false : null);

    const authorLink = card.find('.apphub_CardContentAuthorName a').first();
    const mini = card.find('.apphub_friend_block').first().attr('data-miniprofile');
    const steamid = steamIdFromMiniprofile(mini);
    const owned = /([\d,]+)\s+products? in account/i.exec(card.find('.apphub_CardContentMoreLink').first().text());
    const hours = hoursFromText(card.find('.hours').first().text());

    reviews.push({
      recommendationid: paired ? (ids[i] ?? null) : null,
      review: review || null,
      voted_up: voted,
      timestamp_created: parsePostedDate(posted, now),
      // The HTML has no separate "last edited" date; leaving this null is honest, whereas
      // echoing timestamp_created would fabricate an edit history.
      timestamp_updated: null,
      votes_up: countFromPhrase(helpfulText, 'helpful'),
      votes_funny: countFromPhrase(helpfulText, 'funny'),
      comment_count: Number(card.find('.apphub_CardCommentCount').first().text().replace(/,/g, '')) || 0,
      written_during_early_access: earlyAccess,
      author: {
        steamid,
        personaname: authorLink.text().trim() || null,
        profile_url: steamid ? `https://steamcommunity.com/profiles/${steamid}/` : (authorLink.attr('href') || null),
        // The dead API reported playtime in minutes and reviewRow() still divides by 6/10
        // to get hours; the HTML gives one-decimal hours, so convert back rather than
        // changing the row builder.
        playtime_forever: hours != null ? Math.round(hours * 60) : null,
        num_games_owned: owned ? Number(owned[1].replace(/,/g, '')) : null,
      },
    });
  });

  // The Show-More form's id INCREMENTS with every page (MoreContentForm1 on the /reviews/
  // page, MoreContentForm2 on the first AJAX response, and so on), so it must be matched by
  // prefix. Selecting the literal `#MoreContentForm1` silently caps every scrape at two
  // pages while looking exactly like a clean end-of-feed.
  const form = $('form[id^="MoreContentForm"]').first();
  let next = null;
  if (form.length) {
    const fields = {};
    form.find('input[name]').each((_, inp) => {
      const name = $(inp).attr('name');
      // The reviews tab's form also carries every OTHER tab's page counter
      // (workshopitemspage, screenshotspage, discussionspage, ...). They are irrelevant here
      // and only bloat the URL.
      if (/page$/.test(name) && name !== 'p') return;
      if (!(name in fields)) fields[name] = $(inp).attr('value') ?? '';
    });
    // End of feed is "no cursor to follow", not "the page came back short": the /reviews/
    // page silently clamps out-of-range paging instead of erroring, so an empty-looking page
    // is not a usable stop signal on its own.
    if (fields.userreviewscursor) next = { cursor: fields.userreviewscursor, fields };
  }
  return { reviews, next, cardCount: cards.length, idCount: ids.length };
}
