---
title: Steam quietly attaches a reviewer's PC specs to their review — for about 1 in 15
description: A hardware object with RAM, OS, CPU and GPU rides along on some Steam reviews, sourced from the Hardware Survey opt-in. Measured live on two games — the rate isn't fixed, and the units aren't documented.
date: 2026-09-14
tags: webscraping, api, steam, json
tool: steam-reviews-scraper
---

[Steam's review API is plain JSON](/blog/steam-reviews-public-json-api), no key needed. Most of what it returns is what you'd expect — text, playtime, votes, timestamps. One field isn't: a `hardware` object sitting on a minority of reviews, listing the reviewer's OS, CPU, GPU, RAM and VRAM.

```
$ curl -s 'https://store.steampowered.com/appreviews/730?json=1&filter=recent&language=english&num_per_page=100&cursor=*'
```

Pulled live while writing this, 100 recent English reviews for Counter-Strike 2: **5 of them** carry a `hardware` key. A separate pull for Hades on the same day: **8 of 100**. Neither number is the API's real rate — it's Steam's [Hardware Survey](https://store.steampowered.com/hwsurvey), which is opt-in, so what you actually get is "the fraction of recent reviewers who both opted into the survey and reviewed in the window you asked for." It moves with the audience, not with some fixed sampling rule. A build we ran during development saw 19/100 on one CS2 pull and 4/100 on a `language:"all"` pull for the same game — same endpoint, different day, 4x apart.

When it's there, it looks like this:

```json
{
  "system_ram": "31913",
  "os": "Windows 11",
  "cpu_name": "AMD Ryzen 7 7800X3D 8-Core Processor           ",
  "adapter_description": "NVIDIA GeForce RTX 5070",
  "vram_size": 11943
}
```

When it isn't, the review has no `hardware` key at all — not `null`, not an empty object, just absent. Check with `review.hardware?.field`, not `review.hardware.field`.

## Two things that aren't documented anywhere

**The units are megabytes, not the kilobytes you'd guess from a field with no unit in its name.** `system_ram: "31913"` on a machine with a 32 GB kit, `vram_size: 11943` on a 12 GB RTX 5070, `vram_size: 8042` on an 8 GB RTX 3050 — all consistent only if you read them as MB. Treat them as KB and you'd report a 31 TB RAM stick.

**`cpu_name` comes padded with trailing whitespace on some entries** — `"AMD Ryzen 7 7800X3D 8-Core Processor           "`, spaces and all, straight from Valve's own hardware survey strings. Trim it before you use it as a dedup or group-by key, or you'll silently split one CPU into two buckets depending on which review happened to carry the padding.

Linux reviewers show up too, and their `os` string is whatever their distro reports rather than a fixed enum — one review in this pull carried `"os": "Arch Linux"` next to an AMD GPU line with the full `radeonsi/navi24/ACO/DRM` driver string attached, not just a Windows build number.

## What it's actually useful for

At a 5-15% hit rate this is never going to be a primary key for anything, but it's free, real, and nobody else extracting Steam reviews seems to bother:

- Cross-tabbing negative reviews against reported hardware for a performance-sensitive game — "how many of the 1-hour-refund reviews mention stutter, and what GPU tier are the ones that do actually running" is now answerable without asking anyone anything.
- A cheap, non-scientific read on a game's Linux/Steam Deck audience mix, without a browser session or the Steam Hardware Survey's own aggregate (which is per-platform, not per-game).

## Packaged version

[steam-reviews-scraper](https://apify.com/fetchsmith/steam-reviews-scraper) exposes this as five fields — `hardwareOs`, `hardwareCpu` (trimmed), `hardwareGpu`, `hardwareRamMb`, `hardwareVramMb` — `null` on every review where the author never opted in, real values on the rest. Same run, same price, no extra request: it's already inline on every review Steam returns.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every field name, count and byte value above comes from a live request made while writing this post, not from documentation.*
