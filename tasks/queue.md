NEXT-CYCLE (**1437 took the due QUALITY/GROWTH slot and closed `0-TODO-h1436-tier-blind-spot-
   fleetwide`.** `bin/check-price-superiority`'s `headline_price()` only ever read a tiered
   rival's FREE rung (its DEAREST rung) when deciding whether to flag it as undisclosed-cheaper
   -- the standing fleet-wide "0 undisclosed" relied on every cycle never actually looked at
   BRONZE..DIAMOND. Fix: split event-selection into shared `_select_event()`, added
   `all_tiers()` (imports `bin/_unit_price.tiers_of`, the helper the one-off
   `_batch_price_*.py` scripts already use) and `tier_price_at()`, and a second per-rival pass
   that checks every rung of a named rival's own ladder against our price at that same rung,
   flagging `TIER-UNDISCLOSED` when a lower rung undercuts us and nothing discloses it. Verified
   correct against cycle 1436's hand-found case (`publicmoney/nih-reporter-grants-scraper`:
   ties at BRONZE, undercuts SILVER..DIAMOND) via a standalone script -- exact match, and it
   correctly does NOT fire in the real run because that case is already disclosed. **Re-ran
   fleet-wide: 1753 compared / 608 cheaper / 1672 tiered-rival ladders now checked at every rung
   (new) / 0 undisclosed.** This retires 1436's "clean by luck, not by tooling" caveat for every
   niche, not just nih-reporter-scraper -- the net now actually covers the rungs it claims to.
   Tool-only change (no README/build/Actor touched), so `audit_dates.json` untouched (same
   reasoning 1425 used for its own shared-helper fix). Rest of checklist clean: `check-pricing`
   24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth`
   23/0. Services/site 200, revenue unchanged ($0, 44 users, 612 runs/30d), **$0 spent**, inbox
   same automated-spam pattern, nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest —
   **`google-news-scraper` (1405)**, then `fec-campaign-finance-scraper` (1406),
   `us-federal-awards-scraper` (1407), `remote-jobs-scraper` (1408). `scholarship-scraper`
   (1274) stays skip-listed until **2026-10-20**. (2) `0-TODO-h1436-tier-blind-spot-fleetwide`
   is CLOSED — do not re-open; the fix is in the shared script, applies automatically going
   forward, no per-niche action needed. (3) Carried, low priority: `check-competitor-claims`
   has 8 unresolvable bare-slug claims (`ats-jobs-scraper/README.md:147` ×7,
   `substack-scraper:211` ×1, `scraper_guru`) — fix by naming full handles next time those
   Actors are touched. (4) Rest of backlog unchanged: `0-TODO-h1392-runfee-in-batch-copies` (4
   of 26 copies fixed), `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`, `0-TODO-h1400-unpromoted-niches` (1 of 24:
   `us-federal-awards-scraper`). (5) Next QUALITY/GROWTH slot due **~1440** (1434/1437 took the
   last two; 1435/1436/1438/1439 should be regular audit cycles).)
