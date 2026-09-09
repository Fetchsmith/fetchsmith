import { Actor } from 'apify';
await Actor.init();
await Actor.pushData({ ok: true, note: 'FetchSmith placeholder actor' });
await Actor.exit();
