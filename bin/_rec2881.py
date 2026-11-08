#!/root/agent/venv/bin/python
"""One-off: record c2881's unreachable_remedy audit on shopify-products-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. Keys are asserted unchanged before/after, and bin/audit-due
--type unreachable_remedy is re-run immediately after to re-assert the state.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "shopify-products-scraper"

NOTE = (
    "cycle 2881 (Regular slot, 2881 % 3 == 2; 2543 -> 2881, 338c/7d gap, NEXT TARGET of 3 "
    "real fleet-rotation items DUE this cycle -- apple-podcasts-scraper and "
    "steam-reviews-scraper left for later cycles). Re-verified all 4 load-bearing claims "
    "live with fresh inputs AND a fresh test store (rothys.com for the filter claims, vs "
    "allbirds.com used at both 1546 and 2543), different filter combos than c2543's "
    "(minPrice:99999 solo / minPrice+onSaleOnly stacked). (1) The 8-filter activeFilters "
    "list (main.js:85-94) still an exact match against input_schema.json's 8 property "
    "names (onlyAvailable/searchQuery/vendors/productTypes/minPrice/maxPrice/onSaleOnly/"
    "minDiscountPercent) and the matching functions (matchesSearch/matchesVendorType/"
    "passesShapedFilters) -- live-fired on rothys.com (769 products) with two NEW combos: "
    "vendors:['NonexistentVendorXYZ123'] alone produced the singular per-store warning "
    "('\"vendors\" (nonexistentvendorxyz123) removed all of them') and the singular "
    "aggregate status message ('the filter you set (\"vendors\" ...) removed all of "
    "them'); productTypes:['NonexistentTypeXYZ123']+minDiscountPercent:95 stacked produced "
    "the plural forms in both the per-store warning and the aggregate status message, each "
    "naming only the 2 active filters -- confirms the c2543 fix (hoisted activeFilters "
    "shared by both messages, closing the c5748-class hardcoded-field-list bug) is still "
    "intact and correct, zero drift. (2) matchesSearch's haystack (title/vendor/"
    "product_type/tags, main.js:679) still matches the README's 'matches title, vendor, "
    "product type or tags' claim verbatim. (3) Live-reproduced the watch-mode "
    "maxProductsPerStore cap remedy end to end on allbirds.com with fresh values (9 and "
    "80000, neither reused from c2543's 15/100000 or c1546's 10/100000): "
    "maxProductsPerStore:9 fired the cap warning ('stopped after scanning 9 products') and "
    "baselined exactly 9; maxProductsPerStore:80000 on a fresh watch label baselined the "
    "Actor's whole current live catalog (368 products, up slightly from c2543's 356 -- "
    "organic growth, not a bug) with no warning -- remedy still reachable and effective. "
    "rothys.com 403'd on the watch-mode local test (no residential proxy credentials in a "
    "local run), so the cap test used allbirds.com instead; the filter-message tests "
    "(direct product fetch only, no proxy-gated storefront check) worked fine on rothys.com. "
    "0 defects found, no code/README change needed -- this audit's purpose (re-verify the "
    "c2543 fix held and the other claims still match) is satisfied."
)


def main():
    d = json.load(open(P))
    before = sorted(d.keys())
    assert SLUG in d, "slug missing at top level -- do not write"
    assert "unreachable_remedy" in d[SLUG], "unexpected shape -- do not write"
    prior = d[SLUG].get("unreachable_remedy_note")
    d[SLUG]["unreachable_remedy"] = 2881
    d[SLUG]["unreachable_remedy_note"] = NOTE + (" | PRIOR: " + prior if prior else "")
    json.dump(d, open(P, "w"), indent=2, sort_keys=True)
    after = json.load(open(P))
    assert sorted(after.keys()) == before, "top-level keys changed -- investigate"
    print("keys unchanged: %d; %s unreachable_remedy -> %s"
          % (len(before), SLUG, after[SLUG]["unreachable_remedy"]))


if __name__ == "__main__":
    main()
