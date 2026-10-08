# B01-B02 final financial replay

Cutoff 8 October 2026. [Inputs](Inputs.json), [deterministic builder](Scenario_Builder.py), [results](Financial_Results.json), and [evidence](Evidence.json). All 29 inherited source objects are preserved exactly. The nine C-series objects include legacy calculations; those embedded outputs are historical and are NOT used for this replay. Read the new results for the current 90% basis.

## Basis and evidence boundary

90% of purchase price, 4% annual interest, 35 years. Five-year hold with eleven paid months each year; month 1 is vacant. Monthly common coverage deducts the full standard instalment and fee proxy. Annual cash also deducts other operating allowances and vacancy. Principal is counted once and reconciled to terminal debt. Entry includes 10% equity, a 5% acquisition-cost allowance and stated refurbishment. Disposal allowance is 3%. These pre-tax allowances are not quotations, actual lender offers or proof that unpriced obligations are zero.

Fees combine planning service/sinking allowances where the split is unavailable. The user's management-only standard cannot be certified without the bill. An 8% equity hurdle, RM500,000 starting cash and RM150,000 protected reserve are illustrative, not user finances or mandated return. No base rent growth, refinancing, salary rescue or catalyst appreciation is assumed.

The new cases test older residential substitutes: Astaka's bare purchase against an older partly furnished rental; Prima's partly furnished family format; Damai's index-only family offer; Arena's two-bedroom sale against a differently described rental. These mismatches remain decision holds. Neither 6% gross nor a positive monthly balance validates the property or parcel.

## All selected expressions on one basis

| ID | Price | Gross % | Monthly standard | Entry cash | Annual full-cost cash | Year-5 debt | Nominal recovery sale | Sale for 8% equity | Flat-price profit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C01 M Vertica | 489,000 | 5.89 | 101 | 93,350 | -2,984 | 408,167 | 532,408 | 581,430 | -42,106 |
| C02 Shamelin Star | 700,000 | 4.46 | -589 | 130,000 | -11,474 | 584,288 | 795,523 | 871,763 | -92,657 |
| C03 EkoCheras duplex | 520,000 | 5.31 | -122 | 93,000 | -5,566 | 434,043 | 572,035 | 623,736 | -50,474 |
| C04 Aster Type B | 540,000 | 5.33 | -102 | 101,000 | -5,423 | 450,737 | 596,752 | 652,187 | -55,050 |
| C05 Maxim Residences | 480,000 | 6.00 | 137 | 97,000 | -2,553 | 400,655 | 526,208 | 576,517 | -44,822 |
| C06 Riana South | 595,000 | 5.45 | -71 | 109,250 | -5,353 | 496,645 | 652,225 | 711,641 | -55,508 |
| C07 Green Residence | 540,000 | 4.44 | -552 | 106,000 | -10,423 | 450,737 | 627,680 | 691,005 | -85,050 |
| C08 Windows on the Park large | 900,000 | 4.67 | -936 | 180,000 | -17,138 | 751,228 | 1,048,367 | 1,155,299 | -143,916 |
| C09 Scot Pine | 498,000 | 5.30 | -235 | 114,700 | -7,414 | 415,679 | 585,000 | 649,234 | -84,390 |
| KV01 Maxim Residences | 380,000 | 6.32 | 186 | 77,000 | -2,171 | 317,185 | 417,569 | 457,687 | -36,442 |
| KV02 Lavile Kuala Lumpur | 699,000 | 5.49 | 115 | 119,850 | -4,826 | 583,453 | 749,931 | 814,001 | -49,403 |
| KV03 Akasa | 410,000 | 5.27 | -64 | 81,500 | -4,726 | 342,226 | 461,192 | 506,283 | -49,656 |
| KV04 You Vista | 450,000 | 5.33 | -73 | 87,500 | -5,279 | 375,614 | 504,647 | 553,301 | -53,008 |
| KV05 Emerald Residence | 390,000 | 4.62 | -374 | 78,500 | -8,150 | 325,532 | 458,536 | 505,916 | -66,480 |
| KV06 Windows on the Park | 480,000 | 4.25 | -513 | 92,000 | -10,493 | 400,655 | 561,981 | 618,544 | -79,522 |
| KV07 Citizen 2 | 430,000 | 5.30 | -64 | 79,500 | -5,062 | 358,920 | 478,074 | 522,594 | -46,632 |
| R201 Kuchai Avenue | 359,999 | 6.00 | 95 | 74,000 | -3,055 | 300,490 | 401,820 | 441,424 | -40,566 |
| R202 OUG Parklane | 312,000 | 5.77 | -23 | 66,800 | -4,180 | 260,426 | 358,891 | 396,195 | -45,484 |
| R203 Desa Green | 345,000 | 5.57 | -15 | 66,750 | -3,938 | 287,971 | 385,989 | 423,022 | -39,760 |
| R204 Endah Promenade | 298,000 | 6.44 | 152 | 64,700 | -1,930 | 248,740 | 333,084 | 366,892 | -34,031 |
| R205 Aurora Suites Bukit Jalil | 350,000 | 6.17 | 175 | 72,500 | -1,857 | 292,144 | 385,493 | 423,039 | -34,428 |
| R206 Trion KL | 579,999 | 5.59 | 109 | 107,000 | -4,035 | 484,124 | 630,206 | 687,068 | -48,701 |
| R243 Shamelin Star | 515,000 | 5.13 | -152 | 97,250 | -6,427 | 429,869 | 576,551 | 631,244 | -59,705 |
| R244 Emerald Hills | 570,000 | 4.42 | -471 | 105,500 | -10,157 | 475,777 | 651,612 | 714,422 | -79,164 |
| R245 Landmark Residence 2 | 268,000 | 5.82 | 2 | 60,200 | -3,196 | 223,699 | 309,152 | 342,123 | -39,917 |
| R301 Desa Green 715-sf two-bedroom control | 430,000 | 4.74 | -314 | 79,500 | -7,622 | 358,920 | 491,270 | 538,592 | -59,432 |
| R302 The Tropika 732-sf two-bedroom control | 650,000 | 5.17 | -130 | 122,500 | -7,003 | 542,553 | 721,719 | 789,403 | -69,567 |
| R303 M Oscar 708-sf two-bedroom control | 528,000 | 5.23 | -84 | 99,200 | -5,709 | 440,720 | 586,045 | 640,905 | -56,304 |
| R304 Silk Sky 484-sf compact control | 250,000 | 6.24 | 104 | 52,500 | -1,855 | 208,674 | 278,813 | 306,568 | -27,949 |
| R362 Astaka Heights 1115-sf older family control | 388,000 | 4.95 | -276 | 88,200 | -7,074 | 323,863 | 461,271 | 512,170 | -71,073 |
| R363 Prima Midah Heights 1460-sf mature family control | 550,000 | 3.93 | -742 | 107,500 | -13,101 | 459,084 | 651,637 | 718,621 | -98,588 |
| R364 Damai Hillpark 1020-sf family index control | 390,000 | 5.23 | -114 | 83,500 | -5,230 | 325,532 | 448,639 | 495,236 | -56,880 |
| R365 Arena Green 730-sf residential two-bedroom control | 268,000 | 5.82 | 72 | 65,200 | -2,596 | 223,699 | 311,214 | 345,937 | -41,917 |

Eleven of 33 expressions pass the simplified monthly calculation; six meet the preferred 6% gross scenario. **None has nonnegative annual base cashflow.** R205 and R304 remain component/use-held and do not enter eligible investment rankings. R303 and R364 carry index-only offer holds. All 33 remain G0 STOP / G9 Defer; no counting convention creates Deploy.

The older alternatives change product choice, not the common standard. R365 adds a small advertised residential two-bedroom lead to Bukit Jalil, but its RM72 monthly surplus becomes a RM2,596 annual deficit. A RM100 rent reduction makes even monthly coverage negative. R362 has more family space than the selected Shamelin720 but lower rent, older fit-out exposure and a RM7,074 annual deficit. R363's large usable family format has the weakest new base carry. R364 lowers the A05 entry quantum, yet still needs an independently verifiable offer and better income-to-price relation.

## New-case operating boundaries

| ID | Rent for monthly coverage | Rent for 6% gross | Rent for annual cash neutrality | Price for monthly coverage | Price for 6% gross | Price for annual neutrality |
|---|---:|---:|---:|---:|---:|---:|
| R362 | 1,876 | 1,940 | 2,243 | 318,697 | 320,000 | 240,069 |
| R363 | 2,542 | 2,750 | 2,991 | 363,867 | 360,000 | 276,037 |
| R364 | 1,814 | 1,950 | 2,175 | 361,358 | 340,000 | 280,638 |
| R365 | 1,228 | 1,340 | 1,536 | 286,075 | 260,000 | 213,720 |

These are mechanical constraints under fixed assumptions, **not fair values, offers or a measured margin of safety**. The full results contain the same boundaries for all 33 expressions. Unresolved divergence increases required evidence and safety margin; an unsupported percentage haircut is not a substitute for a valid reference value.

## Package, price and cost branches

| Parent / branch | Entry cash | Monthly standard | First-year cash | Nominal recovery sale | Flat-price profit |
|---|---:|---:|---:|---:|---:|
| R362 / astaka_fee300 | 88,200 | -246 | -6,714 | 459,415 | -69,273 |
| R362 / astaka_fee380 | 88,200 | -326 | -7,674 | 464,364 | -74,073 |
| R362 / astaka_fitout50k | 108,200 | -276 | -7,074 | 481,889 | -91,073 |
| R363 / prima_ff2200_plus20k_fitout | 127,500 | -342 | -8,701 | 649,575 | -96,588 |
| R363 / prima_ff2900_plus35k_fitout | 142,500 | 358 | -1,001 | 625,348 | -73,088 |
| R364 / damai_old400k_index | 85,000 | -154 | -5,708 | 461,256 | -59,418 |
| R364 / damai_ff435k_rent1900 | 80,250 | -93 | -5,182 | 483,764 | -47,301 |
| R364 / damai_216300_auction_proxy | 92,445 | 578 | -5,423 | 274,337 | -56,296 |
| R365 / arena_rent1200 | 65,200 | -28 | -3,696 | 316,884 | -47,417 |
| R365 / arena_advertised132fee | 65,200 | 100 | -2,260 | 309,482 | -40,237 |
| R365 / arena_fee220 | 65,200 | 12 | -3,316 | 314,925 | -45,517 |
| R365 / arena_old255k_offer | 63,250 | 124 | -1,974 | 294,812 | -38,618 |
| R365 / arena_fitout45k | 85,200 | 72 | -2,596 | 331,832 | -61,917 |

Prima's RM2,200 fully furnished branch funds RM20,000 extra fit-out; its RM2,900 branch funds RM35,000 extra and remains a different-size upper asking control. Even the latter has approximately RM1,001 annual negative carry and RM73,088 flat-price loss. A renovated unit may be a better home without justifying the capital required to earn that rent.

The Damai RM216,300 branch is an **auction-reserve diagnostic**, from a 1,050-sf Bumi-labelled cohort, not the selected 1,020-sf ordinary expression. It adds RM60,000 refurbishment and six initially vacant months; first-year cash is negative, later-year cash can become positive, but unknown possession, arrears, eligibility, winning price and lending prevent investable ranking. This is a counterexample to permanent rejection of a project, not evidence of an available bargain.

Arena's older RM255,000 quote exceeds 6% gross at assumed RM1,300 rent but still has negative full-cost carry and flat-price profit. Its 726-sf/two-bath offer is not the selected 730-sf/one-bath parcel. Advertised RM132 fees omit a verified sinking split; old RM79 text is excluded from the base.

## Stress, terminal buyer and no-sale capacity

Each case has base, low/high rent, 5.5% interest, rent -20%, fees +20%, twelve months initially rent-free, RM30,000 works in month 24, bank valuation -15%, 25-year loan, 72-month delayed exit, and an extra RM1,200 annual/RM5,000 exit cost buffer. Two combined paths use 5.5%, rent -20%, fees +20%, six paid months in year one and RM30,000 immediate works, over twelve and sixty months. Those scenarios are not worst-case bounds.

The frozen output's standard balance deliberately remains on the original common basis during stress; use scenario cashflow or the separate actual-instalment/fee metric for the shocked balance. Bank valuation stress lends 90% of 85% of price; this does not replace the standard 90% baseline.

| New case | Combined first-year burn | Minimum cash from illustrative RM500,000 |
|---|---:|---:|
| R362 | 51,735 | 360,065 |
| R363 | 60,699 | 331,801 |
| R364 | 50,363 | 366,137 |
| R365 | 43,767 | 391,033 |

There are 475 evaluated paths including 13 package branches. **479 of 528 two-expression paths preserve the synthetic RM150,000 reserve; 49 do not.** These include alternative units within the same project and are stress diagnostics, not a recommended portfolio. Final programme allocation must deduplicate projects and account for shared tenant, credit, supply, operator and capex exposures.

The investor-exit table values unchanged operating income at illustrative 5%, 6% and 7% required operating yields; these are not observed cap rates or the user's 6% gross preference. It also shows buyer cash and instalments at the recovery price under 90%/4%/35 and an additional 70%/5.5%/25 credit stress. A payment calculation does not prove buyer ability or willingness. The legacy frozen 80% future-buyer field is retained and distinctly labelled.

Twenty selected comparisons produce 180 independent rent-grid cells; 13 comparisons reverse annual cash leaders. Rent bounds are explicit scenarios, not observed probability distributions; the C-series +/-RM200 bounds are analyst sensitivities. Identity and rights holds override arithmetic ranks. Household utility can differ even where cashflow is equal.

## Decision

For ordinary-income investigation, retain the modest-surplus usable-unit leads and separately resolve component-held compact leads. Current-shortfall expressions are the lowest research tier, not permanently rejected. A transition thesis needs a causal transmission mechanism, dated evidence, a falsification point and funded carry. None is automatically financed by assumed rent growth. The no-purchase option remains available; no capital allocation is approved by this replay.
