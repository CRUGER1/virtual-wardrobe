# Launch Proof data pull: cheese squishy (US, ATVPDKIKX0DER)

Pulled 2026-10-15. Data collection only: no analysis, no verdict. Read-only throughout: no campaigns, listings or ads were created or changed. The only things created were two Brand Analytics report requests, which are read jobs.

## Preflight

| Source | Result |
|---|---|
| SP-API (LWA + marketplaceParticipations) | OK, ATVPDKIKX0DER participating |
| Ads API US profile | OK. Env default 3445291785923240 (Hose Haven US) has **no product ads**, so bids were pulled on 158730453104901 (Avolstore US) |
| Keepa | **Not available.** No Keepa MCP server in this session and no Keepa API key in the environment. Tokens used: **0** |
| Amazon Selling Partner MCP | Proxy refused CONNECT (403). Not used; direct SP-API worked |

## Rows per file

| File | Rows |
|---|---|
| aba_terms.csv | 3466 |
| ads_bids.csv | 28 |
| ads_keyword_recs.csv | 300 |
| catalog.csv | 328 |
| fees.csv | 332 |
| keepa.csv | 0 |
| keepa_history.csv | 0 |
| master.csv | 328 |
| pricing.csv | 328 |

## Steps

| # | Step | Status | Notes |
|---|---|---|---|
| 1 | Catalog search | OK | 7 seeds × 100 ASINs = 700 hits, **328 unique**. `relationships` added to includedData to get parent_asin. Empty: parent_asin 117 (no variation parent), sales_rank 15, item_weight 210, release_date 299, product_site_launch_date 1 |
| 2 | Pricing (getItemOffersBatch) | OK | 321 Success, 7 NoBuyableOffers. Buy box price present 316, lowest price present 320. One batch hit QuotaExceeded and succeeded on retry |
| 3 | Fees (getMyFeesEstimates) | Partial | 329 of 332 OK. Priced at buy box, else lowest offer; 8 ASINs with no price were not requested. Assumes FBA (IsAmazonFulfilled=true). **3 failed twice** with InvalidParameterValue: B0H6PSQTGN, B0H6PVFKZR, B0GQSXDFFQ. **size_tier is not returned by this API**, so that column is empty. comparators (rule: title contains 'cheese' AND 'squish', lowest browse-node sales rank): ['B0GTZ43D24', 'B0H7PWTPTV', 'B0GXHVJYJH'] ranks ['16', '27', '34'] node ['Squeeze Toys', 'Squeeze Toys', 'Executive Desk Toys']. Note: the three ranks come from different browse nodes and are not directly comparable |
| 4 | Keepa | **Failed** | No Keepa access in this session (see preflight). keepa.csv and keepa_history.csv are header-only. All Keepa-derived fields in master.csv are empty |
| 5 | Brand Analytics search terms | OK | Brand Registry present; both monthly reports DONE. 2026-09: 3,521,339 rows scanned, 2,906 terms kept. 2025-09: 3,371,105 scanned, 560 kept. Filter: term contains 'squish' OR 'cheese stress' OR 'cheese fidget'. Top-3 clicked ASIN fields are empty where the report had fewer than 3 for a term. Seed terms present as exact rows (search frequency rank): 'cheese squishy' 2026-09=1485, 2025-09=597865; 'cheese squishies' 2026-09=383832, 2025-09=absent; 'squishy cheese' 2026-09=15229, 2025-09=absent; 'mouse and cheese squishy' 2026-09=absent, 2025-09=absent; 'cheese stress ball' 2026-09=1111221, 2025-09=absent; 'cheese fidget toy' 2026-09=absent, 2025-09=absent; 'squishy toys' 2026-09=609, 2025-09=5947 |
| 6 | Ads bid + keyword recommendations | Partial | Theme-based bid recs (v4): 21 rows, all 7 seeds × exact/phrase/broad, low/median/high. Keyword recs v5 returned 429 (gateway throttle) on 3 attempts; v4 worked: 7 seed rows, broad only, **impression share and rank came back null** for every seed. The 100 recommended keywords are driven by the ASIN used (a body trimmer) and are saved separately in ads_keyword_recs.csv. They are not cheese-related. ASIN used: **B0GQ3BTLNL** (Avolstore, RAIZEL body trimmer) |
| 7 | master.csv | OK | Joined on asin: catalog + pricing + fees at current price + Keepa columns (empty). Form rule below. **near_zero_sales is left empty for all rows**: the rule depends on monthlySold, which was never queried, so writing `true` would record a missing pull as a sales fact |

## Form classification rule

```
form rule (title only, case-insensitive, first match wins):
 1 keychain            : 'keychain' | 'key chain' | 'keyring' | 'key ring'
 2 cheese_with_mice_set: 'cheese' AND whole word mouse|mice|rat|rats
 3 slow_rising         : 'slow rising' | 'slow rise' | 'slow-rising'
 4 stress_ball         : 'stress ball' | 'squeeze ball' | 'squishy ball'
 5 single_cheese       : 'cheese'
 6 other               : everything else
 dims NOT used in this pass: classification is title-only. Rules 1, 3 and 4 do not require 'cheese', so non-cheese items from the 'squishy toys' control seed can land in keychain/slow_rising/stress_ball.
```

| form | listings | of which title contains 'cheese' |
|---|---|---|
| slow_rising | 99 | 68 |
| single_cheese | 89 | 89 |
| other | 61 | 0 |
| stress_ball | 56 | 36 |
| cheese_with_mice_set | 20 | 20 |
| keychain | 3 | 3 |

## Requested headline figures

- **Top 3 by monthlySold:** not available. monthlySold comes from Keepa, which did not run. Free route: the "N+ bought in past month" line under the title on each product page.
- **Listings with near_zero_sales:** not available, for the same reason.
- **First seen within the last 24 months (Keepa first-seen):** not available. As a stand-in, Amazon's own catalog field `product_site_launch_date` is on 327 of 328 listings, and **280** of those fall on or after 2024-10-15. This is a different field from Keepa's first-seen date and is not substituted into the Keepa columns.

## To close the gaps

- Keepa: add the key to this cloud environment as `KEEPA_API_KEY` (environment settings → Edit → environment variables / network secrets). A new session picks it up, and steps 4 and 7 can then be re-run.
- Ads keyword recs v5: retry later. It returned 429 Too Many Requests on every attempt today.
- 3 fee failures: try the FBA Revenue Calculator by hand for those ASINs.

Raw API responses and a per-call log are in `raw/`.
