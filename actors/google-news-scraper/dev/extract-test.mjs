import { gotScraping } from 'got-scraping';
import { makeArticleFetcher } from '/root/agent/actors/google-news-scraper/src/article.js';
const http = (url, o={}) => gotScraping({ url, timeout:{request:30000}, retry:{limit:2}, headers:{'accept-language':'en-US'}, ...o });
const f = makeArticleFetcher({ http, bodyMaxChars: 20000, log: { debug: (m)=>console.log('dbg:',m) } });
const urls = [
  'https://www.bbc.com/news/articles/c8xe4z1q0v0o',
  'https://apnews.com/hub/climate',
  'https://www.theguardian.com/environment/2026/jan/01/x',
  'https://techcrunch.com/',
];
for (const u of process.argv.slice(2).length ? process.argv.slice(2) : urls) {
  const r = await f(u);
  console.log(u.slice(0,60), '=>', r.articleFetchStatus, r.articleBodySource||'', 'words:', r.articleWordCount||0, '| author:', r.articleAuthor, '| kw:', (r.articleKeywords||[]).slice(0,3).join('/'));
  if (r.articleBody) console.log('   ', r.articleBody.slice(0,140).replace(/\n/g,' '));
}
