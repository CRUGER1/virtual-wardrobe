# Launch Proof data pull: cheese squishy (US, ATVPDKIKX0DER)

Pulled 2026-10-15 (Keepa re-run the same day in a second session, once a key was added). Data collection only: no analysis, no verdict. Read-only throughout: no campaigns, listings or ads were created or changed. The only things created were two Brand Analytics report requests, which are read jobs.

## Preflight

| Source | Result |
|---|---|
| SP-API (LWA + marketplaceParticipations) | OK, ATVPDKIKX0DER participating |
| Ads API US profile | OK. Env default 3445291785923240 (Hose Haven US) has **no product ads**, so bids were pulled on 158730453104901 (Avolstore US) |
| Keepa | Re-run: OK via `KEEPA_API_KEY`. Basic plan, 300 tokens at start, refill 5/min. Tokens used: **329** (1 probe + 328 ASINs). First run had no key and used 0 |
| Amazon Selling Partner MCP | Proxy refused CONNECT (403). Not used; direct SP-API worked |

## Rows per file

| File | Rows |
|---|---|
| aba_terms.csv | 3466 |
| ads_bids.csv | 28 |
| ads_keyword_recs.csv | 300 |
| catalog.csv | 328 |
| fees.csv | 332 |
| keepa.csv | 328 |
| keepa_history.csv | 18157 |
| master.csv | 328 |
| pricing.csv | 328 |

## Steps

| # | Step | Status | Notes |
|---|---|---|---|
| 1 | Catalog search | OK | 7 seeds × 100 ASINs = 700 hits, **328 unique**. `relationships` added to includedData to get parent_asin. Empty: parent_asin 117 (no variation parent), sales_rank 15, item_weight 210, release_date 299, product_site_launch_date 1 |
| 2 | Pricing (getItemOffersBatch) | OK | 321 Success, 7 NoBuyableOffers. Buy box price present 316, lowest price present 320. One batch hit QuotaExceeded and succeeded on retry |
| 3 | Fees (getMyFeesEstimates) | Partial | 329 of 332 OK. Priced at buy box, else lowest offer; 8 ASINs with no price were not requested. Assumes FBA (IsAmazonFulfilled=true). **3 failed twice** with InvalidParameterValue: B0H6PSQTGN, B0H6PVFKZR, B0GQSXDFFQ. **size_tier is not returned by this API**, so that column is empty. comparators (rule: title contains 'cheese' AND 'squish', lowest browse-node sales rank): ['B0GTZ43D24', 'B0H7PWTPTV', 'B0GXHVJYJH'] ranks ['16', '27', '34'] node ['Squeeze Toys', 'Squeeze Toys', 'Executive Desk Toys']. Note: the three ranks come from different browse nodes and are not directly comparable |
| 4 | Keepa | Partial | Re-run with the key. `/product` (domain=1, stats=90, history=1, days=730), batches of up to 100, ordered by Toys & Games display-group rank (unranked last); waited for token refill between batches. **328 of 328 ASINs returned.** monthlySold present on 251, absent on 77 (Keepa has no 'bought in past month' value for them). current_rank = Keepa's current main sales rank (Toys & Games), empty for 16. listed_since = Keepa `listedSince` (empty for 1), first_seen = Keepa `trackingSince` (all 328). coupon_history = Keepa `couponHistory` (131 ASINs; `$x` = amount off, `x%` = percent off, `none` = coupon removed). deal_history = Keepa lightning-deal price history (13 ASINs); Keepa's product call has no other deal history. **rating and review_count are empty**: Keepa only returns them with `rating=1`, which costs up to 1 extra token per ASIN (~650 tokens, about 2 hours of refill on this plan), so it was not run. keepa_history.csv: top 10 by monthlySold (ties broken by lower current rank; 17 ASINs are tied at 10,000, so the last 3 places are decided by rank), from 2024-10-15, one row per change point with only the changed column filled. price = Keepa NEW (lowest new offer incl. 3P), not buy box. Points where Keepa records -1 (no rank / no new offer) are left out, so gaps in a series mean no data for that period. Raw responses: `raw/keepa_raw_0..3.json.gz` |
| 5 | Brand Analytics search terms | OK | Brand Registry present; both monthly reports DONE. 2026-09: 3,521,339 rows scanned, 2,906 terms kept. 2025-09: 3,371,105 scanned, 560 kept. Filter: term contains 'squish' OR 'cheese stress' OR 'cheese fidget'. Top-3 clicked ASIN fields are empty where the report had fewer than 3 for a term. Seed terms present as exact rows (search frequency rank): 'cheese squishy' 2026-09=1485, 2025-09=597865; 'cheese squishies' 2026-09=383832, 2025-09=absent; 'squishy cheese' 2026-09=15229, 2025-09=absent; 'mouse and cheese squishy' 2026-09=absent, 2025-09=absent; 'cheese stress ball' 2026-09=1111221, 2025-09=absent; 'cheese fidget toy' 2026-09=absent, 2025-09=absent; 'squishy toys' 2026-09=609, 2025-09=5947 |
| 6 | Ads bid + keyword recommendations | Partial | Theme-based bid recs (v4): 21 rows, all 7 seeds × exact/phrase/broad, low/median/high. Keyword recs v5 returned 429 (gateway throttle) on 3 attempts; v4 worked: 7 seed rows, broad only, **impression share and rank came back null** for every seed. The 100 recommended keywords are driven by the ASIN used (a body trimmer) and are saved separately in ads_keyword_recs.csv. They are not cheese-related. ASIN used: **B0GQ3BTLNL** (Avolstore, RAIZEL body trimmer) |
| 7 | master.csv | OK | Joined on asin: catalog + pricing + fees at current price + Keepa columns (rating and review_count empty, see step 4). Form rule below. **near_zero_sales recomputed** with the rule `true if monthlySold is empty or < 50`: 77 true, 251 false. All 77 are true because monthlySold is empty; none has a value under 50, since 50 is the lowest value Amazon publishes |

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

- **Top 3 by monthlySold (all 328 listings):**

  | asin | monthlySold | Keepa rank | brand | form | buy box | title |
  |---|---|---|---|---|---|---|
  | B0DG2VRFV7 | 50,000 | 5 | Mantyplay | other | 9.99 | 30 Pack Squishy Toys, Kawaii Squishies Party Favors |
  | B07HDX46HS | 30,000 | 19 | Crayola | stress_ball | 11.99 | Crayola Globbles Fidget Toy, 6ct, Sticky Stress Ball |
  | B0GPY41JGK | 30,000 | 14 | Schylling | other | (none) | Schylling NeeDoh Squishmas Advent Calendar |

  All three come from the 'squishy toys' control seed and none has 'cheese' in the title. For reference, the top 3 whose title contains 'cheese':

  | asin | monthlySold | Keepa rank | brand | form | buy box |
  |---|---|---|---|---|---|
  | B0GTZ43D24 | 10,000 | 94 | Kaimaizhe | single_cheese | 9.99 |
  | B0H7PRJVD9 | 10,000 | 214 | LAVKUHY | single_cheese | 9.99 |
  | B0GY7YN8BZ | 9,000 | 466 | QPNGKT | stress_ball | 8.99 |

- **Listings with near_zero_sales:** **77 of 328** (71 of the 216 with 'cheese' in the title). By form: single_cheese 26, slow_rising 20, cheese_with_mice_set 15, stress_ball 10, other 4, keychain 2.
- **First seen within the last 24 months (Keepa `trackingSince` on or after 2024-10-15):** **283 of 328**. On Keepa `listedSince` it is 280 of 326 (2 have no listedSince).
- Note: Amazon's 'bought in past month' figure is published in rounded steps (50, 100, ... 1,000, 2,000 ...), and it can be shared across variations of one parent. The two Horizon Group Gelli Gels colours (B0G36VXNGX, B0G36Z353F), for example, both show 10,000.

## To close the gaps

- Keepa rating and review count: re-request with `rating=1` (about 650 tokens on the basic plan, roughly 2 hours of refill).
- Ads keyword recs v5: retry later. It returned 429 Too Many Requests on every attempt today.
- 3 fee failures: try the FBA Revenue Calculator by hand for those ASINs.

Raw API responses and a per-call log are in `raw/`.
