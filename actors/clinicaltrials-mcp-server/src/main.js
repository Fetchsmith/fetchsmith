// Standby-mode MCP server. Pattern verified against Apify's own `ts-mcp-empty` template
// (actor.json `usesStandbyMode`/`webServerMcpPath`, readiness-probe header, `Actor.charge`
// per tool call) -- see notes/LEARNINGS.md cycle 2758. One real tool: search_clinical_trials,
// reusing clinicaltrials-scraper's verified API base/params.
import express from 'express';
import cors from 'cors';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import * as z from 'zod';
import { gotScraping } from 'got-scraping';
import { Actor, log } from 'apify';

await Actor.init();

const API = 'https://clinicaltrials.gov/api/v2/studies';
// pageSize clamp matches clinicaltrials-scraper (cycle 120): pageSize=1001 returns 200 with only
// the first 1000 honored, so a caller-supplied value above this would silently under-deliver.
const MAX_PAGE_SIZE = 1000;

async function searchClinicalTrials({ condition, intervention, maxResults }) {
    const params = new URLSearchParams();
    if (condition) params.set('query.cond', condition);
    if (intervention) params.set('query.intr', intervention);
    params.set('pageSize', String(Math.min(Math.max(Number(maxResults) || 10, 1), MAX_PAGE_SIZE)));
    const url = `${API}?${params.toString()}`;
    const res = await gotScraping({ url, responseType: 'json', timeout: { request: 20000 } });
    const studies = res.body?.studies ?? [];
    return studies.map((s) => {
        const id = s.protocolSection?.identificationModule;
        const status = s.protocolSection?.statusModule?.overallStatus ?? null;
        return {
            nctId: id?.nctId ?? null,
            title: id?.briefTitle ?? null,
            status,
            url: id?.nctId ? `https://clinicaltrials.gov/study/${id.nctId}` : null,
        };
    });
}

const getServer = () => {
    const server = new McpServer(
        { name: 'clinicaltrials-mcp-server', version: '0.1.0' },
        { capabilities: { logging: {} } },
    );

    server.registerTool(
        'search_clinical_trials',
        {
            description: 'Search ClinicalTrials.gov (official NIH registry) by condition and/or intervention.',
            inputSchema: {
                condition: z.string().optional().describe('Medical condition, e.g. "asthma"'),
                intervention: z.string().optional().describe('Drug, device or procedure, e.g. "semaglutide"'),
                maxResults: z.number().optional().describe('Max studies to return (default 10, max 1000)'),
            },
        },
        async ({ condition, intervention, maxResults }) => {
            await Actor.charge({ eventName: 'tool-call' });
            const studies = await searchClinicalTrials({ condition, intervention, maxResults });
            return {
                content: [{ type: 'text', text: JSON.stringify(studies, null, 2) }],
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
    log.info(`clinicaltrials-mcp-server listening on ${Actor.config.get('standbyPort')}`);
});
