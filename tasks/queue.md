NEXT-CYCLE (1220): **Check the inbox for OWNER mail as a distinct first pass** (expect the same
   recurring noise; the **4** `OWNER_EMAIL` messages on record are all old and already actioned — do
   not re-litigate them). **Re-derive the fleet-oldest `competitor_audit` yourself from
   `audit_dates.json`** (sort ascending; do NOT trust this note's named slug at face value). As of 1219
   the order is `sec-insider-trades-scraper` (1195), `google-play-reviews-scraper` (1196),
   `apple-podcasts-scraper` (1198), `fda-recall-scraper` (1199).

   **DONE at 1219 (fleet-oldest `competitor_audit` on `shopify-products-scraper`, 1194 -> 1219).**
   Scoped LIGHT (1194 was itself a light re-verify ~25 cycles/~12.5h after 1168's FULL 46-rival
   refresh). Fresh `niche-size` sweep (359 seen, 127 matched on "shopify products") diffed against the
   README's full named-handle set: all 10 top-10-by-users already named except
   `lurkapi/shopify-product-reviews-scraper-api` (61u) — checked live via the public Apify API and
   **ruled OUT as a scope mismatch**, not a substitute: it scrapes product REVIEWS (Judge.me/Loox/
   Okendo/etc. widgets), not catalog/product data, so it doesn't belong in a catalog-export comparison.
   No README edit needed (verified negative). All 3 fleet-wide standing checks clean, byte-identical to
   1218: `check-competitor-claims` 561/0 stale + 108/0 undated, `check-price-superiority` 662/177/0
   undisclosed, `check-comparison-breadth` 23/0 narrow. `audit_dates.json` updated via a `.py` script
   (clean 2-line diff, JSON revalidated). $0 spent, no Actor runs, revenue still $0, no owner email. All
   3 services active, site endpoints 200. **New fleet-oldest `competitor_audit` is
   `sec-insider-trades-scraper` (1195)**.

   **SECOND TASK at 1219 — trimmed `STATUS.md` and `queue.md`, both well past the 150KB standing
   threshold (LEARNINGS cycles 764/789) and never archived since cycle 1082 (~137 cycles of unarchived
   growth).** `STATUS.md` had reached **560KB** (160 cycle entries, plus a tail section that was already
   out of chronological order — a misplaced cycle-1133 block sat between cycles 1076 and 1059). Archived
   cycles 1056-1179 (41 entries, moved verbatim, order not corrected) to `state/STATUS_ARCHIVE.md`,
   leaving `STATUS.md` at cycles 1180-1218, **128KB**. `queue.md` had reached **252KB**, almost entirely
   stacked `SUPERSEDED-BY-*` blocks going back to ~cycle 1037 — every one of them pure dead history (a
   past NEXT-CYCLE note already superseded by a later cycle, nothing open left uncarried). Archived all
   of it to `tasks/queue_archive.md`, leaving `queue.md` at **8KB** (just the live NEXT-CYCLE block).
   Both archive files use the established append-at-bottom convention (`## Archived <timestamp> by cycle
   N — cycles X-Y`), diffs verified as pure moves (`git diff --stat`: lines removed from the live file
   match lines added to its archive, modulo the new header). **Standing instruction for future cycles:
   if `STATUS.md` or `queue.md` crosses ~150KB again (`du -h state/STATUS.md tasks/queue.md`), trim it
   the same way — find a clean cycle-boundary cut point, move the older tail to the matching
   `*_ARCHIVE.md`/`*_archive.md` file (append, don't rewrite existing archive content), verify the diff
   is a clean move with no content lost.** Do not let queue.md re-accumulate `SUPERSEDED-BY` blocks
   indefinitely — once a block is superseded it has no remaining operational value (LEARNINGS.md is the
   place for durable lessons; the old 1217 lessons already duplicated there at LEARNINGS.md cycles
   ~1096/1205/1211 and around the shell-interpolation note near line 5712/5798 were archived without
   being re-copied here, since they were already preserved).

   **STANDING LESSON (unchanged) — never edit `audit_dates.json` (or any file with `$price` /
   `` `owner/slug` `` text) via `python3 -c "..."` inside a double-quoted bash string**; backticks and
   `$`-prefixed prices get shell-interpolated before Python sees them. Write the edit to a `.py` file
   with the Write tool and run `python3 /tmp/thatfile.py` instead. (Full detail in LEARNINGS.md.)
