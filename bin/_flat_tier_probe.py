#!/root/agent/venv/bin/python
"""c2740: hunt a SECOND live instance of the c2737 flat-rival `every_tier` bug.

The bug: a flat-priced rival has one key in `unit_tiers` (labeled FREE by
_unit_price.py); `all(t in OURS and ut[t] < OURS[t] for t in ut)` therefore only
compares it against OURS["FREE"] -- our DEAREST rung -- and prints every_tier=True
even when the rival is dearer than our deeper rungs.

It can only produce a false positive where OUR OWN price is TIERED. Of the 10
Family-A pricers, only these 3 are: ats3, rjs, uktft2. Offline, $0, no API.
"""
import json, os

NICHES = {
 "ats3 (ats-jobs-scraper)": ("/tmp/ats_prices3.json",
   {"FREE":0.001,"BRONZE":0.00085,"SILVER":0.00075,"GOLD":0.0007,"PLATINUM":0.0007,"DIAMOND":0.0007}),
 "rjs (remote-jobs-scraper)": ("/tmp/rjs_prices.json",
   {"FREE":0.0015,"BRONZE":0.0013,"SILVER":0.0011,"GOLD":0.001,"PLATINUM":0.001,"DIAMOND":0.001}),
 "uktft2 (uk-find-a-tender-scraper)": ("/tmp/uktft_prices2.json",
   {"FREE":0.003,"BRONZE":0.0028,"SILVER":0.0026,"GOLD":0.0025,"PLATINUM":0.0025,"DIAMOND":0.0025}),
}

total_flat = total_bad = 0
for label, (path, OURS) in NICHES.items():
    if not os.path.exists(path):
        print(f"{label}: COHORT MISSING ({path}) -- cannot test offline"); continue
    rows = json.load(open(path))
    flat = [r for r in rows if len(r.get("unit_tiers") or {}) == 1]
    # genuinely-free / FREE-model rows are NOT the bug: $0 really does beat every rung
    flat_priced = [r for r in flat if list(r["unit_tiers"].values())[0] > 0]
    bad = []
    for r in flat_priced:
        v = list(r["unit_tiers"].values())[0]
        legacy = r.get("every_tier")
        truth = all(v < OURS[t] for t in OURS)          # the correct rung-for-rung read
        if legacy and not truth:
            dearer = sorted(t for t in OURS if v >= OURS[t])
            bad.append((r["handle"], v, dearer, r.get("users")))
    total_flat += len(flat_priced); total_bad += len(bad)
    print(f"\n{label}: {len(rows)} rows, {len(flat)} flat ({len(flat_priced)} flat-and-priced)")
    print(f"  MIS-FLAGGED every_tier: {len(bad)}")
    for h, v, dearer, u in bad:
        print(f"    {h:<48} ${v:<10} users={u}  actually DEARER than: {','.join(dearer)}")

print(f"\nTOTAL across the 3 tiered-OURS niches: {total_flat} flat-priced rivals, "
      f"{total_bad} mis-flagged every_tier")
