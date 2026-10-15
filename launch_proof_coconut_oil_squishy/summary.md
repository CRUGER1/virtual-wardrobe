# Launch Proof data pull: coconut oil squishy (US, ATVPDKIKX0DER)

Pulled 2026-10-15. Data collection only: no analysis, no verdict. Read-only throughout: no campaigns, listings or ads were created or changed. Same pipeline and file layout as `launch_proof_cheese_squishy/`.

Seeds: `coconut oil squishy`, `coconut oil squishies`, `squishy coconut oil`, `coconut squishy`, `coconut oil butter squishy`, `coconut oil stress ball`, `squishy toys` (broad control, same as the cheese pull).

## Rows per file

| File | Rows |
|---|---|
| catalog.csv | 323 |
| pricing.csv | 323 |
| fees.csv | 320 |
| ads_bids.csv | 21 |
| keepa.csv | 323 |
| keepa_history.csv | 17843 |
| master.csv | 323 |

Brand Analytics search terms are **not repeated here**: `launch_proof_cheese_squishy/aba_terms.csv` already holds every term containing 'squish' for 2026-09 and 2025-09, which includes all coconut oil squishy terms (55 terms containing 'coconut' in 2026-09; `coconut oil squishy` has search frequency rank 291).

## Steps

| # | Step | Status | Notes |
|---|---|---|---|
| 1 | Catalog search | OK | 7 seeds × 100 ASINs, **323 unique**. **110 of them are also in the cheese pull.** Empty: parent_asin 107, sales_rank 13, item_weight 207, release_date 301, product_site_launch_date 1, package dims 11 |
| 2 | Pricing (getItemOffersBatch) | OK | 308 Success, 15 NoBuyableOffers. Buy box present 305, lowest price present 308. One 429 succeeded on retry |
| 3 | Fees (getMyFeesEstimates) | Partial | 310 of 320 OK. Priced at buy box, else lowest offer; ASINs with no price were not requested. Assumes FBA. **10 failed twice** with InvalidParameterValue, all recent B0H… listings: B0HHZR6SWK, B0HJWB46J6, B0HC66B96N, B0HHZJ32BB, B0H9PVXNND, B0HF719NPW, B0HFWXMWP7, B0HKCT9YM2, B0H9KBDTZQ, B0HFWZDVLK. size_tier not returned by this API. Comparators (rule: title contains 'coconut' AND 'squish', lowest browse-node sales rank): B0H7PRJVD9 (rank 3, Executive Desk Toys), B0GVJDX674 (12, Squeeze Toys), B0HG5127RZ (12, Executive Desk Toys), each at $7.99 / $9.99 / $12.99 / $14.99. The ranks come from different browse nodes and are not directly comparable |
| 4 | Keepa | Partial | `/product` (domain=1, stats=90, history=1, days=730). 110 ASINs reused from the cheese pull made the same day; 213 fetched. **Tokens used: 213.** 323 of 323 returned. monthlySold present on 262, absent on 61. current_rank empty 18, listed_since empty 1. coupon_history on 130, lightning-deal history on 12. **rating and review_count empty** (need `rating=1`, extra tokens). keepa_history.csv: top 10 by monthlySold, from 2024-10-15, same format as the cheese pull (17 ASINs tied at 10,000, so the last places go by lower current rank) |
| 6 | Ads bid recommendations | OK | Theme-based v4, all 7 seeds × exact/phrase/broad, low/median/high. Profile 158730453104901 (Avolstore US), ASIN used **B0GQ3BTLNL** (body trimmer), as in the cheese pull. Keyword recommendations not re-pulled: for that ASIN they return trimmer keywords |
| 7 | master.csv | OK | catalog + pricing + fees at current price + Keepa. Adds `form`, `coconut_oil` (title contains 'coconut') and `near_zero_sales` (`true` if monthlySold is empty or < 50) |

## Form classification rule

```
form rule (title only, case-insensitive, first match wins):
 1 keychain        : 'keychain' | 'key chain' | 'keyring' | 'key ring'
 2 multipack       : '<n> pack' | '<n>pack' | '<n> pcs' | '<n>pcs' | '<n> pieces' | '<n> count' | '<n>ct' with n >= 2, or 'set of <n>' n >= 2
 3 cheese_shape    : 'cheese'
 4 butter_shape    : 'butter'
 5 fruit_food_shape: apple|strawberry|peach|banana|grape|cherry|lemon|orange|mango|watermelon|avocado|dumpling|bread|toast|cake|donut|cookie|mochi|peanut|potato|egg
 6 ball            : 'ball'
 7 other           : everything else
 coconut_oil column (separate axis): title contains 'coconut'.
 dims NOT used: classification is title-only.
```

Different rule from the cheese pull, because the target here is a material (coconut oil), not a shape. Visible units = sum of Keepa monthlySold.

| form | listings | coconut_oil = true | coconut listings' monthlySold | share of coconut units |
|---|---|---|---|---|
| multipack | 152 | 93 | 40,100 | 27.4% |
| ball | 65 | 60 | 41,250 | 28.2% |
| butter_shape | 47 | 39 | 20,100 | 13.7% |
| fruit_food_shape | 23 | 13 | 3,800 | 2.6% |
| cheese_shape | 18 | 17 | 41,050 | 28.1% |
| other | 18 | 0 | 0 | 0% |

## Requested headline figures

- **Top 3 by monthlySold (all 323):** B0DG2VRFV7 Mantyplay 30 Pack, 50,000; B0GPY41JGK Schylling NeeDoh Advent Calendar, 30,000; B07HDX46HS Crayola Globbles, 30,000. All three are from the 'squishy toys' control seed and none is coconut oil.
- **Top 3 with 'coconut' in the title:**

  | asin | monthlySold | Keepa rank | brand | form | buy box |
  |---|---|---|---|---|---|
  | B0GVJDX674 | 20,000 | 83 | Glyrnur | ball | 9.99 |
  | B0GTZ43D24 | 10,000 | 94 | Kaimaizhe | cheese_shape | 9.99 |
  | B0H7PRJVD9 | 10,000 | 214 | LAVKUHY | cheese_shape | 9.99 |

- **near_zero_sales:** **61 of 323** (58 of the 222 coconut listings). All 61 because monthlySold is empty. By form: multipack 23, butter_shape 23, ball 11, fruit_food_shape 3, cheese_shape 1.
- **First seen within the last 24 months (Keepa `trackingSince` ≥ 2024-10-15):** **305 of 323**. On `listedSince`: 303 of 322.

## Still open

- Keepa rating and review count (`rating=1`), or take them from the Helium 10 X-Ray exports.
- 10 fee failures: FBA Revenue Calculator by hand, or the X-Ray `Fees` column.
- POE exports (no API exists) and Helium 10 X-Ray / trend exports: see the request list in the chat.

Raw API responses and a per-call log are in `raw/`.
