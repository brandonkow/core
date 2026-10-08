# B08 Working01 — financial underwriting

Cutoff: 8 October 2026. All amounts RM. This is conditional scenario arithmetic for nine preserved inputs and four new expressions, not verified rent, value or an executable shortlist. No catchment closes in this working packet. [Inputs](Inputs.json), [results](Financial_Results.json) and [builder](Scenario_Builder.py) are reproducible with the pinned frozen engine/configuration in [the release manifest](Release_Manifest.json).

## Common basis and limitations

Use 90% of purchase price, 4% interest, 35 years for the common rent-minus-full-instalment-minus-management comparison. All fee inputs are unverified combined service/sinking proxies; management-only bills remain unverified. Preferred gross yield is 6%. Fee, other-cost and refurbishment allowances are estimates. No future rent growth, refinancing, guarantee or appreciation is assumed.

Base collections are 11 months per year, with month 1 vacant; no letting until month 2 is implicitly credited. The model pays the complete instalment and operating allowances monthly. Entry cash includes 10% equity, 5% purchase-cost allowance and fit-out; exit deducts 3%. These are pre-tax allowances, not quoted legal/tax/agent costs. Unknown charges, financing eligibility, repair bills and current contracts are not certified zero. A separate cost buffer adds RM1,200/year and RM5,000 at exit. The illustrative 8% equity hurdle is not a user-approved required return.

## Base comparison

| Case | Ask | Monthly rent | Gross | Standard monthly balance | Annual carry | Entry cash | Five-year nominal break-even exit |
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

Six of thirteen bases meet the simplified monthly standard; five reach 6% gross. Only R353 has positive full-year base carry, about RM820. These counts describe unverified assumptions; all thirteen remain G0 STOP / G9 Defer. The inherited inputs retain their dates and limitations rather than being represented as refreshed offers.

## New-case thresholds

Let k be the monthly payment on RM0.90 at 4% over 35 years. Standard coverage requires R >= kP + F; 6% gross requires R >= 0.005P; annual carry neutrality requires R >= 12(kP + F + O)/11. Rearranging yields conditional price constraints. They are not valuation intervals, bids, verified margin of safety or investment permission.

| Case | Rent for standard | Rent for 6% gross | Rent for annual neutrality | Price for standard | Price for 6% gross | Price for annual neutrality |
|---|---:|---:|---:|---:|---:|---:|
| R351 | 1,276 | 1,350 | 1,566 | 326,226 | 300,000 | 254,707 |
| R352 | 1,089 | 1,090 | 1,362 | 170,641 | 180,000 | 111,670 |
| R353 | 1,127 | 1,100 | 1,425 | 313,678 | 300,000 | 237,141 |
| R354 | 1,766 | 1,840 | 2,123 | 376,414 | 360,000 | 293,603 |

R351 requires about RM67 more monthly rent than base for annual neutrality; that small gap does not authenticate its fit-out, parking or current lease. R352 remains negative even when the larger furnished RM1,300 rent proxy is granted with extra fit-out. R353's annual surplus is less than one unmodelled RM100/month expense. R354's apparently inexpensive compact offer still needs about RM2,123 ordinary rent for annual neutrality under these proxies.

## Adverse and favourable competing expressions

| Case | Branch | Entry cash | Annual carry, first year | Nominal break-even exit |
|---|---|---:|---:|---:|
| R351 | FF_1750_with_extra_fitout | 85,500 | 2,019 | 310,077 |
| R351 | higher_FF_360k_1750 | 69,000 | -2,285 | 392,697 |
| R352 | FF_1300_larger_proxy | 67,700 | -685 | 260,915 |
| R352 | higher_bare_290k | 58,500 | -8,528 | 353,815 |
| R353 | higher_ask_285k | 67,750 | -2,289 | 326,888 |
| R353 | initial_vacancy3 | 58,000 | -2,180 | 247,974 |
| R353 | extra_recurring100 | 58,000 | -380 | 251,067 |
| R354 | earlier_470k_PF_no_bay | 95,500 | -8,435 | 546,375 |
| R354 | parking150_monthly | 70,200 | -5,358 | 416,657 |
| R354 | lower_fee200 | 70,200 | -2,358 | 401,193 |

All branch evidence boundaries are in Inputs.json. R351's RM1,750 FF branch includes RM20,000 additional assumed fit-out but still lacks proof of the advertised two bays. R352's RM1,300 evidence is 897sf, not 860sf. R353's RM285k same-marketed-size price control reverses the base annual surplus; three initial vacant months also make year one negative. R354's RM470k older PF offer is not interchangeable with the selected RM368k FF offer; the model keeps both. The RM150/month parking cost and RM200 fee branch are sensitivities, not quotes.

Base low/high rent paths are sensitivity bounds, not confidence intervals: R351 low1400 is an adverse assumption and high1750 is a different furnishing/bay package; R352800/1000 is indexed asking dispersion; R3531400 is an adverse ordinary-rent assumption and1700 is a larger950sf ask; R3541600 is an adverse assumption and2000 is the same old advertisement's conflicting header. The naked high-rent rows retain base fit-out so they are arithmetic upper tests, not validated operating plans.

## Terminal exposure and future buyers

Nominal exit break-even is (entry equity and acquisition/fit-out allowances − cumulative operating cash + remaining debt + exit-extra costs) / 0.97. Principal is counted once. The 8% exit threshold discounts cash monthly. Required prices are burdens that need independent future-buyer support, not projected market outcomes.

| Case | Year-5 debt | Nominal break-even | Exit for illustrative 8% | Flat-price total profit | Operating yield at nominal break-even |
|---|---:|---:|---:|---:|---:|
| R351 | 225,368 | 303,634 | 336,474 | -32,625 | 4.01% |
| R352 | 181,964 | 262,977 | 291,912 | -43,627 | 2.03% |
| R353 | 183,633 | 244,881 | 272,368 | -24,135 | 4.63% |
| R354 | 307,169 | 407,378 | 445,702 | -38,197 | 3.45% |

The investor-exit diagnostics test 5%, 6% and 7% operating yields using 11 months' rent less recurring allowances before financing. These are hypothetical required yields, distinct from the user's 6% gross preference and not measured market cap rates. At 5%, income-only values for R351/R352/R353/R354 are RM243,600/106,800/226,800/280,800, all below their nominal required exits. A resident buyer could pay differently for utility, but demand depth and affordability need evidence; an investor-led exit is also eligible without an invented owner-only requirement.

Future-buyer diagnostics compare 90%/4%/35 years with a separate 70%/5.5%/25-year stress; the 70% case also needs 30% equity plus 5% costs and fit-out. These are cash/payment stresses, not legal LTV limits. Frozen-engine output additionally retains its named 80% future-buyer payment field; it is a distinct sensitivity, not the 70% diagnostic and not the common underwriting standard.

## Forced hold, simultaneous stress and rank reversals

Synthetic RM500,000 cash and RM150,000 protected reserve are inherited comparison settings, not the user's balance sheet. Combined stress: 5.5% rate, rent −20%, fee +20%, only six paid months in year one, RM30,000 works immediately per asset and no sale for 12 months. Later years use 11 collections. The minimum monthly cash path is tested, with no salary/refinance/sale rescue.

| Case | Cash used in stressed first year after entry | Minimum remaining cash | Five-year stressed nominal exit |
|---|---:|---:|---:|
| R351 | 43,259 | 391,241 | 378,997 |
| R352 | 43,412 | 408,888 | 325,695 |
| R353 | 41,320 | 400,680 | 317,388 |
| R354 | 49,183 | 380,617 | 495,429 |

All 78 pairs preserve the synthetic reserve under this defined stress. This generous cash setting does not discriminate among pairs and is not evidence of portfolio suitability. University exposure, financing, fee inflation, tenant churn and geographically linked supply can be correlated. Programme-level portfolio selection remains outstanding.

The 54 low/base/high rent-grid cells cover six pairs in Inputs.json. Within-area contrasts test Evo/MKH, D'Cerrum/Ascotte, Solstice/Arc and Dwiputra/Shaftsbury; cross-area MKH/Arc and Arc/Shaftsbury compare capital opportunity cost, not identical household utility. All remain held before executable ranking. Different condition, eligibility and finance cannot be erased by a cash-coverage leaderboard.

## Verification scope

192 evaluations comprise 13 × 14 standard paths and 10 explicit branches. Closed-form amortisation, principal conservation, independent interest-and-operating-cost break-even, discounted exit and annual-cash identities are checked. Adverse-shock direction is checked where economically monotonic; no blanket monotonic claim is made for shorter financing, lower bank valuations or delayed exit. A six-year hold can reduce nominal break-even while raising the required discounted return burden. Arithmetic checks do not verify market assumptions, titles, leases or outcomes.
