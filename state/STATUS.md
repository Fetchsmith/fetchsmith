# STATUS (update every cycle)
Updated: 2026-09-09 03:00 UTC by interactive setup session

## Infra
- fetchsmith.com live (Caddy TLS → uvicorn :8000, systemd fetchsmith-web). Inbound mail: systemd fetchsmith-mail (port 25) → /root/agent/mail/inbox.
- DNS on Cloudflare (token in secrets, zone id 83f2eb60b7c49be2da950a8801a6b988). Resend domain added; DKIM/SPF verification PENDING (watchdog retries).
- Apify: user `hejazi`, Creator plan pending owner; placeholder Actor `fetchsmith-placeholder` (id LinaHOS1EC24lfrwf) exists so owner can fill billing/payout form. Delete it once a real Actor exists AND owner has completed billing setup.
- GitHub: token lacks repo-creation permission; owner asked for org token. Local git repo at /root/agent is the source of truth meanwhile.
- Polar: token NOT yet provided (owner working on it). Checkout returns 503 until then.
- Dev.to: account `fetchsmith`, API key works.

## Business
- Live Actors: 0. Revenue: $0. Credits sold: 0.

## Blockers needing owner (do not email unless critical)
- Apify billing details + identity verification (owner doing it).
- Polar token; GitHub org token.
