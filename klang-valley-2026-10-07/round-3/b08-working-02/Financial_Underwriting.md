# B08 Working02 — financial underwriting

Cutoff: 8 October 2026. All amounts RM. [Inputs](Inputs.json), [results](Financial_Results.json) and [builder](Scenario_Builder.py) preserve the frozen arithmetic and thirteen prior expressions. All eighteen operating cases remain G0 STOP / G9 Defer. Counts and calculations do not certify market evidence.

## Common basis

The standard remains 90% of purchase price, 4%, 35 years, with rent less full instalment and management. Preferred gross yield remains 6%. Base collections are eleven months each year, with month 1 vacant; operating costs and instalments are paid every month. Entry cash is 10% equity plus a 5% acquisition-cost allowance and fit-out; exit deducts 3%. Actual tax, insurance, legal, repair, financing and tenancy costs are not authenticated. These are pre-tax planning allowances, not zero-cost certifications. Full instalment includes principal once. Combined management/sinking proxies are not verified management-only bills; R357's350 fee is agent-reported and still unverified.

No future rent growth, refinance, guaranteed return or appreciation is assumed. The illustrative8% equity discount rate and synthetic500k cash/150k protected reserve are inherited diagnostics, not the user's actual circumstances or newly imposed Core conditions.

## Base comparison

| Case | Ask | Rent | Gross | Standard monthly balance | Annual carry | Entry cash | Five-year nominal break-even exit |
|---|---:|---:|---:|---:|---:|---:|---:|
| R237 Evo SOHO Suite | 248,000 | 1,300 | 6.29% | 82 | -2,239 | 52,200 | 278,764 |
| R238 D'Cerrum | 250,000 | 1,000 | 4.80% | -216 | -5,515 | 52,500 | 297,679 |
| R239 Dwiputra Residences | 520,000 | 2,300 | 5.31% | -72 | -5,806 | 103,000 | 583,581 |
| R240 Geo Bukit Rimau | 500,000 | 1,900 | 4.56% | -372 | -8,770 | 100,000 | 578,554 |
| R241 Habitus Denai Alam | 390,000 | 1,650 | 5.08% | -164 | -5,780 | 73,500 | 441,165 |
| R242 GAIA Residences | 380,000 | 1,500 | 4.74% | -244 | -6,591 | 77,000 | 440,353 |
| R247 The Parque Residences | 470,000 | 1,500 | 3.83% | -673 | -11,735 | 90,500 | 558,231 |
| R248 Alanis Residence | 210,000 | 1,200 | 6.86% | 163 | -1,162 | 51,500 | 239,791 |
| KV14 Solstice @ Pan'gaea | 200,000 | 1,200 | 7.20% | 223 | -324 | 45,000 | 220,164 |
| R351 MKH Boulevard II | 270,000 | 1,500 | 6.67% | 224 | -731 | 65,500 | 303,634 |
| R352 Ascotte Boulevard | 218,000 | 900 | 4.95% | -189 | -5,085 | 47,700 | 262,977 |
| R353 The Arc | 220,000 | 1,500 | 8.18% | 373 | 820 | 58,000 | 244,881 |
| R354 Shaftsbury Putrajaya | 368,000 | 1,800 | 5.87% | 34 | -3,558 | 70,200 | 407,378 |
| R355 Alanis Residence compact | 249,000 | 1,200 | 5.78% | 28 | -2,667 | 57,350 | 287,139 |
| R356 Aman 1 Tropicana Urban Homes | 338,000 | 1,500 | 5.33% | -97 | -4,823 | 75,700 | 393,756 |
| R357 Habitus Denai Alam original compact control | 360,000 | 1,300 | 4.33% | -485 | -9,155 | 74,000 | 433,264 |
| R358 GAIA Residences larger family control | 500,000 | 1,700 | 4.08% | -572 | -10,730 | 90,000 | 578,348 |
| R359 Alanis Residence family control | 365,000 | 1,600 | 5.26% | -135 | -5,374 | 79,750 | 424,006 |

Seven bases pass the simplified monthly comparison; five reach6% gross. Only inherited R353 has positive annual base carry, about820, and its existing100/month cost buffer already reverses that. None of the five new bases has positive annual carry. Historical inputs retain their original evidence dates and are not represented as refreshed executable offers.

## New-case income constraints

Let k be the monthly payment on0.90 at4%/35years. Standard rent >= kP+F;6% gross rent >=0.005P; annual-neutral rent >=12(kP+F+O)/11. The rearranged prices are constraints under unverified inputs, not fair-value intervals, executable bids or validated margins of safety.

| Case | Rent for standard | Rent for6% gross | Rent for annual neutrality | Price for standard | Price for6% gross | Price for annual neutrality |
|---|---:|---:|---:|---:|---:|---:|
| R355 | 1,172 | 1,245 | 1,442 | 255,962 | 240,000 | 193,226 |
| R356 | 1,597 | 1,690 | 1,938 | 313,678 | 300,000 | 237,141 |
| R357 | 1,785 | 1,800 | 2,132 | 238,396 | 260,000 | 168,550 |
| R358 | 2,272 | 2,500 | 2,675 | 356,339 | 340,000 | 275,619 |
| R359 | 1,735 | 1,825 | 2,089 | 331,244 | 320,000 | 252,616 |

## Adversarial and favourable branches

| Case | Branch | Monthly standard | First-year carry | Entry cash | Nominal five-year break-even |
|---|---|---:|---:|---:|---:|
| R355 | lower_index228k | 111 | -1,663 | 54,200 | 260,645 |
| R355 | unmatched_project_floor193k | 251 | 11 | 48,950 | 216,487 |
| R355 | extra_recurring100_compact | 28 | -3,867 | 57,350 | 293,325 |
| R356 | restricted_bumi330k | -65 | -4,440 | 74,500 | 383,662 |
| R356 | rent1700_extra_fitout | 103 | -2,623 | 90,700 | 397,879 |
| R357 | optimistic_fee200 | -335 | -7,355 | 74,000 | 423,986 |
| R357 | rent1400_fee200 | -235 | -6,255 | 74,000 | 418,316 |
| R358 | rent2400_extra_fitout | 128 | -3,030 | 110,000 | 559,276 |
| R359 | quarantined_lelong_worded300k | 125 | -2,266 | 60,000 | 331,689 |
| R359 | initial_vacancy3_family | -135 | -8,574 | 79,750 | 427,305 |

The193k Alanis branch deliberately tests a weak unmatched project-floor lead: its annual surplus is only11. It is not an authenticated offer and cannot enter an investable ranking. At228k the compact case still loses1663/year. The330k Aman branch is restricted; the1700 rent branch requires additional fit-out and still loses2623/year. Habitus remains negative even with both higher1400rent and lower200fee. GAIA2400rent and Alanis family300kprice also produce monthly passes with annual losses. Favourable scenarios therefore do not resolve ordinary-income or G0 holds.

The low/high rows in Financial_Results retain base fit-out and are arithmetic bounds, not complete implementation plans. R3551000 and1400 are downside/upside rent sensitivities, not signed leases; R3561300/1700 come from condition-mixed indexes; R3571200 comes from a room-label conflict and1400 from a separate one-bedroom index; R3581500 is a downside assumption and2400 a two-bay asking control; R3591400 is downside and1800 an older two-bay ad with a size typo. Branches with explicit extra fit-out avoid treating a rent upgrade as free, but costs/rights are still unverified.

## Exit burden and forced hold

Nominal break-even = (entry cash − cumulative operating cash + remaining debt + exit-extra costs) /0.97. It is a required future price, not a projected sale. The frozen engine separately calculates monthly-discounted8% required exits, zero-rent first12months,30k works,5.5% interest,20% lower rent,20% higher fees,15% lower bank valuation,25year loan,12month sale delay, and an extra1200/year plus5000exit-cost buffer.

| New case | Year5 debt | Nominal break-even | Flat-price total profit | Operating yield at break-even | Combined-stress required exit |
|---|---:|---:|---:|---:|---:|
| R355 | 207,840 | 287,139 | -36,995 | 3.22% | 356,156 |
| R356 | 282,128 | 393,756 | -54,083 | 2.88% | 474,463 |
| R357 | 300,491 | 433,264 | -71,066 | 1.86% | 513,645 |
| R358 | 417,349 | 578,348 | -75,998 | 2.28% | 673,779 |
| R359 | 304,665 | 424,006 | -57,235 | 2.85% | 508,507 |

Operating yield is eleven months' rent less recurring allowances before debt, divided by exit price. Illustrative5/6/7% investor-required operating yields are not the user's6% gross preference or observed market cap rates. Both investor and resident exits remain eligible; each needs price, depth and financing evidence. Separate90%/4%/35year versus70%/5.5%/25year future-buyer diagnostics test payment and entry cash. The engine's separate80% field is retained unchanged, not conflated with either standard or70%stress.

All153 two-case joint no-sale cash paths preserve the synthetic150k reserve under the defined first-year joint shock. That cannot validate allocation: capital is synthetic, shocks are limited, unit rights remain held, and several pairs are alternative expressions in the same project. Ninety-nine unequal-rent grid cells test eleven selected comparisons. Portfolio aggregation must deduplicate R248/R355/R359, R241/R357 and R242/R358 rather than count independent geographic diversification. The full-programme correlation/portfolio audit remains outstanding.

## Forward control: Kanopi, no current rent booked

| Price expression | Rent for standard | Rent for6%gross | Rent for annual neutrality |
|---|---:|---:|---:|
| 590,888 | 2,705 | 2,954 | 3,191 |
| 675,888 | 3,043 | 3,379 | 3,560 |

B08-T01 uses official current590888 headline and675888 brochure ordinary minimum as two unresolved price expressions, with analyst350fee/220other allowances. These are requirements once stabilised, not a forecast rent or completed acquisition model. The2026 press statement targetsQ3 2027; brochure legal text saysNovember2028. Neither is authenticated selected-SPA timing or CCC. Do not book rent before legal possession/fit-out/letting. Progressive drawdown, interest, incentive eligibility, delivery delay and selected inventory need a separate dated pre-VP cash model if the opportunity advances.
