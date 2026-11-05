// Standby-mode MCP server. Same verified pattern as clinicaltrials-mcp-server (cycle 2759):
// actor.json `usesStandbyMode`/`webServerMcpPath`, readiness-probe header, `Actor.charge` per
// tool call -- see notes/LEARNINGS.md cycle 2758 for the Apify `ts-mcp-empty` template it was
// checked against. One real tool: search_news, reusing google-news-scraper's verified RSS feed
// URLs and item parser (actors/google-news-scraper/src/main.js `parseRss`).
import express from 'express';
import cors from 'cors';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import * as z from 'zod';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';
import { Actor, log } from 'apify';

await Actor.init();

// Named topic sections, copied from google-news-scraper's input_schema (verified live there,
// cycles 1798/264). The first 8 are the ones Google links in its own nav; the rest it serves
// but never links. An unknown code returns an empty feed rather than an error, so the tool
// validates against this list instead of passing it through.
const TOPICS = [
    'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SCIENCE', 'SPORTS', 'HEALTH',
    'POLITICS', 'ECONOMY', 'REAL_ESTATE', 'JOBS', 'EDUCATION', 'AUTOS', 'MOVIES', 'MUSIC',
    'CELEBRITIES', 'ARTS', 'SOCCER', 'BASKETBALL',
];
const MAX_LIMIT = 100;
// got applies `timeout.request` per ATTEMPT, and got's own internal retries multiply it (~4x),
// so a plain `timeout: {request}` is not a bound on one call -- cycle 2646 proved this for real
// on remote-jobs-scraper and the fleet fix was AbortSignal, which tears the socket down
// externally. An MCP tool call is synchronous to the caller's agent, so a real bound matters
// more here than in a batch run.
const REQUEST_MS = 15000;

// Google News RSS titles always arrive as "Headline - Publisher" (verified live on 204/204 items,
// cycle 264), which is noise once `publisher` already carries it.
const stripSourceSuffix = (title, source) => (source && title.endsWith(` - ${source}`) ? title.slice(0, -(source.length + 3)).trim() : null);
const hostOf = (u) => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return null; } };

function parseRss(xml) {
    const $ = cheerio.load(xml, { xml: true });
    return $('item').map((_, el) => {
        const $el = $(el);
        const descHtml = $el.find('description').text();
        const $d = cheerio.load(descHtml || '');
        const title = $el.find('title').text().trim();
        const source = $el.find('source').text().trim() || null;
        const sourceUrl = $el.find('source').attr('url') || null;
        // The <description> is not a summary: it is either a single <a> holding the headline
        // again, or an <ol> of the same story as covered by several publishers, each <a> paired
        // with a grey <font> naming that publisher. Entries after the first are genuinely new
        // data, and are the single most agent-useful field here -- "who else covered this".
        const $links = $d('a');
        const $fonts = $d('font');
        const related = $links.slice(1).map((i, a) => ({
            title: $d(a).text().trim() || null,
            publisher: $fonts.eq(i + 1).text().trim() || null,
        })).get().filter((r) => r.title);
        const pubDate = $el.find('pubDate').text().trim();
        const parsed = pubDate ? new Date(pubDate) : null;
        return {
            title: stripSourceSuffix(title, source) || $links.first().text().trim() || title,
            publisher: source,
            publisherDomain: hostOf(sourceUrl),
            // Not resolved to the publisher's own URL on purpose: decoding Google's redirect
            // costs an extra request per article and Google rate-limits it (google-news-scraper
            // carries the whole proxy/backoff apparatus for that). This link works as-is, and an
            // MCP tool call is synchronous to the caller's agent -- latency beats a prettier URL.
            // Buyers who need resolved publisher URLs want the batch Actor, not this tool.
            url: $el.find('link').text().trim(),
            publishedAt: parsed && !Number.isNaN(parsed.getTime()) ? parsed.toISOString() : null,
            relatedCoverage: related,
        };
    }).get();
}

async function searchNews({ query, topic, limit, language, country }) {
    const hl = language || 'en-US';
    const gl = country || 'US';
    const ceid = `${gl}:${hl.split('-')[0]}`;
    const n = Math.min(Math.max(Number(limit) || 10, 1), MAX_LIMIT);
    const url = topic
        ? `https://news.google.com/rss/headlines/section/topic/${encodeURIComponent(topic)}?hl=${hl}&gl=${gl}&ceid=${ceid}`
        : `https://news.google.com/rss/search?q=${encodeURIComponent(query)}&hl=${hl}&gl=${gl}&ceid=${ceid}`;
    const res = await gotScraping({
        url,
        headers: { 'accept-language': hl },
        timeout: { request: REQUEST_MS },
        retry: { limit: 1 },
        signal: AbortSignal.timeout(REQUEST_MS),
    });
    return parseRss(res.body).slice(0, n);
}

const getServer = () => {
    const server = new McpServer(
        { name: 'google-news-mcp-server', version: '0.1.0' },
        { capabilities: { logging: {} } },
    );

    server.registerTool(
        'search_news',
        {
            description: 'Search Google News for current news articles by keyword, or browse one of Google News\' '
                + 'built-in topic sections. Returns headline, publisher, publish time, a working article link and '
                + 'the same story as covered by other publishers. Exactly one of `query` or `topic` is required. '
                + 'Google search operators work inside `query` (e.g. "tesla when:1d", "site:reuters.com inflation", '
                + '"ai -nvidia").',
            inputSchema: {
                query: z.string().optional().describe('Keyword or phrase to search, e.g. "openai funding". Google News search operators (when:, site:, -word, OR, quotes) are supported.'),
                topic: z.enum(TOPICS).optional().describe('Browse a topic section instead of searching. One of: WORLD, NATION, BUSINESS, TECHNOLOGY, ENTERTAINMENT, SCIENCE, SPORTS, HEALTH, POLITICS, ECONOMY, REAL_ESTATE, JOBS, EDUCATION, AUTOS, MOVIES, MUSIC, CELEBRITIES, ARTS, SOCCER, BASKETBALL.'),
                limit: z.number().optional().describe('Max articles to return (default 10, max 100). Google serves about 100 per feed.'),
                language: z.string().optional().describe('Language code, e.g. "en-US", "de", "fr" (default "en-US").'),
                country: z.string().optional().describe('Country edition, e.g. "US", "GB", "DE" (default "US").'),
            },
        },
        async ({ query, topic, limit, language, country }) => {
            // Charge only for a call that actually returned at least one article -- the fleet's
            // standing "no result, no charge" rule, and the same order cycle 2760's varied_test
            // forced on clinicaltrials-mcp-server (charging before the fetch billed buyers
            // $0.005 for upstream errors and for empty searches).
            if (!query && !topic) {
                return {
                    isError: true,
                    content: [{
                        type: 'text',
                        text: 'search_news needs either `query` (a keyword search) or `topic` (a Google News section). '
                            + 'Not charged.',
                    }],
                };
            }
            if (query && topic) {
                // Google serves these from two different endpoints; a topic feed ignores the
                // query entirely, so honouring both would silently drop the caller's keyword and
                // return a plausible-looking wrong answer. Refuse, and do not charge.
                return {
                    isError: true,
                    content: [{
                        type: 'text',
                        text: 'search_news takes `query` OR `topic`, not both: Google serves topic sections from a '
                            + 'different feed that ignores keywords, so a topic call would silently drop your query. '
                            + 'To search within a subject, put it in `query` (e.g. "inflation when:7d"). Not charged.',
                    }],
                };
            }
            let articles;
            try {
                articles = await searchNews({ query, topic, limit, language, country });
            } catch (error) {
                log.warning('search_news upstream failure', { error: String(error) });
                return {
                    isError: true,
                    content: [{
                        type: 'text',
                        text: `Google News did not answer (${String(error)}). Not charged -- retry the call.`,
                    }],
                };
            }
            if (articles.length > 0) await Actor.charge({ eventName: 'tool-call' });
            return {
                content: [{ type: 'text', text: JSON.stringify(articles, null, 2) }],
            };
        },
    );

    return server;
};

const app = express();
app.use(express.json());
app.use(cors({ origin: '*', exposedHeaders: ['Mcp-Session-Id'] }));

app.get('/', (req, res) => {
    if (req.headers['x-apify-container-server-readiness-probe']) {
        res.writeHead(200);
        res.end('ok');
        return;
    }
    res.status(404).end();
});

app.post('/mcp', async (req, res) => {
    const server = getServer();
    try {
        const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
        await server.connect(transport);
        await transport.handleRequest(req, res, req.body);
        res.on('close', () => {
            transport.close();
            server.close();
        });
    } catch (error) {
        log.error('Error handling MCP request', { error: String(error) });
        if (!res.headersSent) {
            res.status(500).json({ jsonrpc: '2.0', error: { code: -32603, message: 'Internal server error' }, id: null });
        }
    }
});

app.listen(Actor.config.get('standbyPort'), () => {
    log.info(`google-news-mcp-server listening on ${Actor.config.get('standbyPort')}`);
});
