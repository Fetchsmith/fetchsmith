#!/root/agent/venv/bin/python
"""One-off: record c2869's enum_audit on shopify-products-scraper.

Keyed d[slug]['enum_audit'] -- slug at the TOP level, per the c2866 tooling trap.
Keys are asserted unchanged before/after, and bin/audit-due --type enum_audit is
re-run immediately after to re-assert the state.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "shopify-products-scraper"

NOTE = (
    "c2869: no registered vocab-screen probe for this Actor (both declared enums are OUR OWN "
    "vocabularies, not upstream ones), so audited from the schema outward. `watchEvents` (8 "
    "values: new/priceDrop/priceIncrease/wentOnSale/saleEnded/backInStock/outOfStock/delisted) "
    "-- grepped main.js: all 8 are reachable (WATCH_EVENTS at line 106, each pushed somewhere "
    "in the change-detection block lines 288-300 or the delisted sweep lines 1019-1117), none "
    "dead. `detailLevel` (basic/full) -- live-reproved on allbirds.com: bulk products.json "
    "carries NONE of barcode/inventory_quantity/inventory_management on a variant (confirmed "
    "absent), while the per-product .js route (what detailLevel:full additionally fetches) "
    "carries all of them with real values (barcode 196942331460, inventory_quantity 0) -- "
    "basic genuinely omits, full genuinely adds, exactly as the README and schema claim. "
    "ONE REAL GAP FOUND AND FIXED: a watchEvents value that isn't one of the 8 fails OPEN, "
    "not closed -- main.js lines 107-111 warn on an unknown value, then if the resulting valid "
    "set is empty (all-bogus input), default back to ALL 8, same as leaving the field empty. "
    "README documented the 8 values and the empty-default behavior but never stated what a "
    "bogus value does -- added one sentence to the watchEvents input-table row (c2869 build) "
    "covering the fail-open behavior. Not reachable via Apify's own select-editor UI (fixed "
    "choices only), only via direct API input, so low-severity but a real precision gap per "
    "the audit checklist's item (d)."
)


def main():
    d = json.load(open(P))
    before = sorted(d.keys())
    assert SLUG in d, "slug missing at top level -- do not write"
    prior = d.get(SLUG, {}).get("enum_audit_note")
    d.setdefault(SLUG, {})["enum_audit"] = 2869
    d[SLUG]["enum_audit_note"] = (
        NOTE + ("  [prior note preserved] " + prior if prior else "")
    )
    json.dump(d, open(P, "w"), indent=2, sort_keys=True)
    after = json.load(open(P))
    assert sorted(after.keys()) == before, "top-level keys changed -- investigate"
    print("keys unchanged: %d; %s enum_audit -> %s"
          % (len(before), SLUG, after[SLUG]["enum_audit"]))


if __name__ == "__main__":
    main()
