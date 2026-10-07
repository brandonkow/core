# Unified financial chain - existing Cheras case replay

Release KV-EXEC-2026-10-07; configuration KV-FIN-90-4-35-v1. Run date 7 October 2026; original evidence cutoff 6 October 2026. No new market research. All price/rent/fee/repair inputs retain their original limitations. This is a scenario replay, not fair value, lender approval or an executable recommendation.

## Common basis and cost boundary

90% of acquisition price, 4% annual rate, 35 years; five-year illustrative hold. Gross yield preferably 6%. Rent is assumed, fee is a combined service/sinking proxy, and actual management-only coverage remains unverified. The baseline has eleven paid months per year, original other-cost and refurbishment allowances, 5% acquisition and 3% disposal allowances. It is pre-tax and excludes unquoted transaction-specific costs and base-case major works. These allowances are not legal fee/tax quotations. An illustrative extra-cost sensitivity adds RM1,200 annually and RM5,000 at exit; it is not a tax estimate.

The 8% equity hurdle is illustrative, not user-approved. Cashflows are discounted monthly at an effective annual 8%, so hurdle results cannot be compared mechanically with the previous end-year approximation. Base first-year vacancy is month 1 and repeats each year. Holding scenarios use month-by-month principal/interest and collections. Standard coverage always retains 90%/4%/35 even in actual-financing stress.

## Entry, coverage, carrying cost and exit

| Case | Entry cash | Standard monthly balance | Annual base cashflow | Year-5 debt | Nominal break-even sale | Sale required for 8% | Flat-price total profit |
|---|---:|---:|---:|---:|---:|---:|---:|
| C01 M Vertica | 93,350 | +101 | -2,984 | 408,167 | 532,408 | 581,430 | -42,106 |
| C02 Shamelin Star | 130,000 | -589 | -11,474 | 584,288 | 795,523 | 871,763 | -92,657 |
| C03 EkoCheras duplex | 93,000 | -122 | -5,566 | 434,043 | 572,035 | 623,736 | -50,474 |
| C04 Aster Type B | 101,000 | -102 | -5,423 | 450,737 | 596,752 | 652,187 | -55,050 |
| C05 Maxim Residences | 97,000 | +137 | -2,553 | 400,655 | 526,208 | 576,517 | -44,822 |
| C06 Riana South | 109,250 | -71 | -5,353 | 496,645 | 652,225 | 711,641 | -55,508 |
| C07 Green Residence | 106,000 | -552 | -10,423 | 450,737 | 627,680 | 691,005 | -85,050 |
| C08 Windows on the Park large | 180,000 | -936 | -17,138 | 751,228 | 1,048,367 | 1,155,299 | -143,916 |
| C09 Scot Pine | 114,700 | -235 | -7,414 | 415,679 | 585,000 | 649,234 | -84,390 |

Required exits are burdens, not predictions or supported ceilings. Flat-price profit counts principal exactly once; loan proceeds are not returns. Financial inputs and unknown costs cannot be promoted to verified zero. Current-shortfall cases remain lowest research priority under the new SOP, not automatic structural Reject.

## Future buyer payment at the required nominal break-even price

| Case | Standard 90% / 4% / 35y payment | Actual-credit stress 80% / 5.5% / 25y payment |
|---|---:|---:|
| C01 | 2,122 | 2,616 |
| C02 | 3,170 | 3,908 |
| C03 | 2,280 | 2,810 |
| C04 | 2,378 | 2,932 |
| C05 | 2,097 | 2,585 |
| C06 | 2,599 | 3,204 |
| C07 | 2,501 | 3,084 |
| C08 | 4,178 | 5,150 |
| C09 | 2,331 | 2,874 |

Lower stressed LTV requires more buyer cash; neither payment establishes buyer depth or loan eligibility. Actual loan terms, title and buyer equity must be resolved.

## Twelve-month forced hold and correlated portfolio stress

Synthetic RM500k starting cash and RM150k protected reserve, not user finances. Immediate RM30k works per asset, rate 5.5%, rent down 20%, no rent in the first six months and no sale for twelve months. Baseline 90% financing. Check the minimum monthly cash path, not only the ending balance. No salary, refinancing or future sale proceeds rescue the path.

| Case | Minimum remaining cash | Reserve pass |
|---|---:|---|
| C01 | 353,809 | Yes, scenario |
| C02 | 305,282 | Yes, scenario |
| C03 | 351,881 | Yes, scenario |
| C04 | 343,201 | Yes, scenario |
| C05 | 350,681 | Yes, scenario |
| C06 | 332,601 | Yes, scenario |
| C07 | 335,681 | Yes, scenario |
| C08 | 242,002 | Yes, scenario |
| C09 | 329,177 | Yes, scenario |

24 of 36 pairs preserve the synthetic reserve under simultaneous asset shocks. This differs from the old 80%/30-year result because entry equity and instalments both change. A pair funding pass does not establish suitable diversification, actual household reserves, debt-service approval or a Deploy. Cash-path details are in Financial_Results.json.

## Five-year and delayed-exit sensitivities

| Case | Scenario | Entry cash | Total carry cashflow | Terminal debt | Nominal break-even | Flat-price profit |
|---|---|---:|---:|---:|---:|---:|
| C01 | rate_5_5pct | 93,350 | -39,805 | 416,248 | 566,394 | -75,072 |
| C01 | rent_down20 | 93,350 | -41,319 | 408,167 | 559,625 | -68,506 |
| C01 | fee_up20 | 93,350 | -19,119 | 408,167 | 536,738 | -46,306 |
| C01 | zero_rent_first12 | 93,350 | -41,319 | 408,167 | 559,625 | -68,506 |
| C01 | works_30k_month24 | 93,350 | -44,919 | 408,167 | 563,336 | -72,106 |
| C01 | bank_valuation_down15 | 159,365 | +2,619 | 346,942 | 519,266 | -29,358 |
| C01 | actual_loan_term25 | 93,350 | -37,381 | 383,347 | 529,977 | -39,748 |
| C01 | exit_delay12 | 93,350 | -17,903 | 400,979 | 528,074 | -37,902 |
| C01 | illustrative_unquoted_cost_buffer | 93,350 | -20,919 | 408,167 | 543,749 | -53,106 |
| C02 | rate_5_5pct | 130,000 | -92,992 | 595,856 | 844,173 | -139,848 |
| C02 | rent_down20 | 130,000 | -85,969 | 584,288 | 825,007 | -121,257 |
| C02 | fee_up20 | 130,000 | -62,169 | 584,288 | 800,471 | -97,457 |
| C02 | zero_rent_first12 | 130,000 | -85,969 | 584,288 | 825,007 | -121,257 |
| C02 | works_30k_month24 | 130,000 | -87,369 | 584,288 | 826,450 | -122,657 |
| C02 | bank_valuation_down15 | 224,500 | -32,264 | 496,645 | 776,710 | -74,408 |
| C02 | actual_loan_term25 | 130,000 | -89,522 | 548,759 | 792,043 | -89,281 |
| C02 | exit_delay12 | 130,000 | -68,843 | 573,999 | 796,744 | -93,841 |
| C02 | illustrative_unquoted_cost_buffer | 130,000 | -63,369 | 584,288 | 806,863 | -103,657 |
| C03 | rate_5_5pct | 93,000 | -54,294 | 442,636 | 608,175 | -85,530 |
| C03 | rent_down20 | 93,000 | -53,131 | 434,043 | 598,117 | -75,774 |
| C03 | fee_up20 | 93,000 | -32,031 | 434,043 | 576,365 | -54,674 |
| C03 | zero_rent_first12 | 93,000 | -53,131 | 434,043 | 598,117 | -75,774 |
| C03 | works_30k_month24 | 93,000 | -57,831 | 434,043 | 602,963 | -80,474 |
| C03 | bank_valuation_down15 | 163,200 | -9,181 | 368,936 | 558,059 | -36,918 |
| C03 | actual_loan_term25 | 93,000 | -51,717 | 407,650 | 569,450 | -47,966 |
| C03 | exit_delay12 | 93,000 | -33,397 | 426,399 | 569,893 | -48,396 |
| C03 | illustrative_unquoted_cost_buffer | 93,000 | -33,831 | 434,043 | 583,375 | -61,474 |
| C04 | rate_5_5pct | 101,000 | -54,594 | 459,660 | 634,282 | -91,454 |
| C04 | rent_down20 | 101,000 | -53,513 | 450,737 | 623,969 | -81,450 |
| C04 | fee_up20 | 101,000 | -31,313 | 450,737 | 601,082 | -59,250 |
| C04 | zero_rent_first12 | 101,000 | -53,513 | 450,737 | 623,969 | -81,450 |
| C04 | works_30k_month24 | 101,000 | -57,113 | 450,737 | 627,680 | -85,050 |
| C04 | bank_valuation_down15 | 173,900 | -7,746 | 383,126 | 582,239 | -40,972 |
| C04 | actual_loan_term25 | 101,000 | -51,917 | 423,328 | 594,068 | -52,446 |
| C04 | exit_delay12 | 101,000 | -32,536 | 442,799 | 594,159 | -52,535 |
| C04 | illustrative_unquoted_cost_buffer | 101,000 | -33,113 | 450,737 | 608,092 | -66,050 |
| C05 | rate_5_5pct | 97,000 | -37,195 | 408,587 | 559,568 | -77,181 |
| C05 | rent_down20 | 97,000 | -39,167 | 400,655 | 553,425 | -71,222 |
| C05 | fee_up20 | 97,000 | -16,967 | 400,655 | 530,538 | -49,022 |
| C05 | zero_rent_first12 | 97,000 | -39,167 | 400,655 | 553,425 | -71,222 |
| C05 | works_30k_month24 | 97,000 | -42,767 | 400,655 | 557,136 | -74,822 |
| C05 | bank_valuation_down15 | 161,800 | +4,448 | 340,557 | 513,308 | -32,309 |
| C05 | actual_loan_term25 | 97,000 | -34,815 | 376,292 | 523,822 | -42,507 |
| C05 | exit_delay12 | 97,000 | -15,321 | 393,599 | 521,567 | -40,320 |
| C05 | illustrative_unquoted_cost_buffer | 97,000 | -18,767 | 400,655 | 537,548 | -55,822 |
| C06 | rate_5_5pct | 109,250 | -57,043 | 506,477 | 693,578 | -95,621 |
| C06 | rent_down20 | 109,250 | -56,464 | 496,645 | 682,844 | -85,208 |
| C06 | fee_up20 | 109,250 | -31,564 | 496,645 | 657,174 | -60,308 |
| C06 | zero_rent_first12 | 109,250 | -56,464 | 496,645 | 682,844 | -85,208 |
| C06 | works_30k_month24 | 109,250 | -56,764 | 496,645 | 683,153 | -85,508 |
| C06 | bank_valuation_down15 | 189,575 | -5,424 | 422,148 | 636,234 | -39,997 |
| C06 | actual_loan_term25 | 109,250 | -54,094 | 466,445 | 649,267 | -52,639 |
| C06 | exit_delay12 | 109,250 | -32,116 | 487,899 | 648,727 | -52,115 |
| C06 | illustrative_unquoted_cost_buffer | 109,250 | -32,764 | 496,645 | 663,565 | -66,508 |
| C07 | rate_5_5pct | 106,000 | -79,594 | 459,660 | 665,210 | -121,454 |
| C07 | rent_down20 | 106,000 | -74,113 | 450,737 | 650,360 | -107,050 |
| C07 | fee_up20 | 106,000 | -56,913 | 450,737 | 632,629 | -89,850 |
| C07 | zero_rent_first12 | 106,000 | -74,113 | 450,737 | 650,360 | -107,050 |
| C07 | works_30k_month24 | 106,000 | -82,113 | 450,737 | 658,608 | -115,050 |
| C07 | bank_valuation_down15 | 178,900 | -32,746 | 383,126 | 613,167 | -70,972 |
| C07 | actual_loan_term25 | 106,000 | -76,917 | 423,328 | 624,996 | -82,446 |
| C07 | exit_delay12 | 106,000 | -62,536 | 442,799 | 630,242 | -87,535 |
| C07 | illustrative_unquoted_cost_buffer | 106,000 | -58,113 | 450,737 | 639,020 | -96,050 |
| C08 | rate_5_5pct | 180,000 | -131,490 | 766,100 | 1,110,917 | -204,590 |
| C08 | rent_down20 | 180,000 | -124,189 | 751,228 | 1,088,058 | -182,416 |
| C08 | fee_up20 | 180,000 | -95,889 | 751,228 | 1,058,883 | -154,116 |
| C08 | zero_rent_first12 | 180,000 | -124,189 | 751,228 | 1,088,058 | -182,416 |
| C08 | works_30k_month24 | 180,000 | -115,689 | 751,228 | 1,079,295 | -173,916 |
| C08 | bank_valuation_down15 | 301,500 | -53,410 | 638,543 | 1,024,179 | -120,454 |
| C08 | actual_loan_term25 | 180,000 | -127,029 | 705,547 | 1,043,893 | -139,576 |
| C08 | exit_delay12 | 180,000 | -102,826 | 737,998 | 1,052,396 | -147,824 |
| C08 | illustrative_unquoted_cost_buffer | 180,000 | -91,689 | 751,228 | 1,059,707 | -154,916 |
| C09 | rate_5_5pct | 114,700 | -62,414 | 423,909 | 619,611 | -117,963 |
| C09 | rent_down20 | 114,700 | -61,271 | 415,679 | 609,949 | -108,590 |
| C09 | fee_up20 | 114,700 | -42,471 | 415,679 | 590,567 | -89,790 |
| C09 | zero_rent_first12 | 114,700 | -61,271 | 415,679 | 609,949 | -108,590 |
| C09 | works_30k_month24 | 114,700 | -67,071 | 415,679 | 615,928 | -114,390 |
| C09 | bank_valuation_down15 | 181,930 | -19,210 | 353,327 | 571,616 | -71,408 |
| C09 | actual_loan_term25 | 114,700 | -59,946 | 390,403 | 582,525 | -81,989 |
| C09 | exit_delay12 | 114,700 | -44,485 | 408,359 | 585,097 | -84,484 |
| C09 | illustrative_unquoted_cost_buffer | 114,700 | -43,071 | 415,679 | 596,340 | -95,390 |

Bank valuation down 15% finances 90% of the reduced value, increasing cash needed; it is a separate actual-finance constraint, not an alternative standard LTV. The delayed exit has 72 months of carry and amortisation. No-uplift is the base; catalysts are not automatic rent growth. No scenario is a worst-case bound.

## Rank robustness: C01 versus C05

Illustrative rent grid RM2,200/2,400/2,600 for each independently; not observed ranges or probability weights. This tests whether small assumption differences can reverse a cash-coverage preference, not which product has better actual buyer demand.

| M Vertica rent | Maxim rent | Coverage leader | M Vertica balance | Maxim balance |
|---:|---:|---|---:|---:|
| 2,200 | 2,200 | C05 | -99 | -63 |
| 2,200 | 2,400 | C05 | -99 | +137 |
| 2,200 | 2,600 | C05 | -99 | +337 |
| 2,400 | 2,200 | C01 | +101 | -63 |
| 2,400 | 2,400 | C05 | +101 | +137 |
| 2,400 | 2,600 | C05 | +101 | +337 |
| 2,600 | 2,200 | C01 | +301 | -63 |
| 2,600 | 2,400 | C01 | +301 | +137 |
| 2,600 | 2,600 | C05 | +301 | +337 |

At equal assumed rents, Maxim's coverage advantage is only RM36/month. That small difference cannot support strong overall superiority with unverified rents, fees and operations. Independent rent/fee evidence has higher next-step value than another qualitative description of the same amenities.

## Verification and status

Checked recurrence against closed-form amortisation, principal conservation, independent interest-plus-cost break-even identity, monthly discounted hurdle, shock direction and rank reversal. The original model/report files are unchanged. No case passes missing G0/unit/governance evidence through this calculation. The full model is now on the approved baseline; the earlier bridge remains a historical calibration.
