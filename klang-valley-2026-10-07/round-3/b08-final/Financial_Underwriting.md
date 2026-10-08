# B08 final financial underwriting

Cutoff: 8 October 2026. [Inputs](Inputs.json), [deterministic builder](Scenario_Builder.py) and [full results](Financial_Results.json) reproduce this comparison using the unchanged [execution engine](../../../execution-release-2026-10-07/financial_engine.py). All prices/rents/costs are conditional case inputs; no model output clears G0. All 20 cases Defer.

The common test remains 90% purchase-price LTV, 4%, 35 years and rent less full instalment plus management proxy. The current combined management/sinking proxies are not authenticated management-only bills. Keep the user's preferred 6% gross distinct from annual full-cost carry and from investor operating yields. Other recurring allowances, eleven paid months, entry fit-out and terminal costs are explicit. Unquoted parcel costs are not known to be zero.

## Base comparison

Amounts RM, rounded. Annual cash includes full principal-and-interest instalments, recurring proxies and one unpaid month; principal is not charged twice. Nominal exit recovers entry equity and carry over five years. The 8% hurdle is a scenario, not an expected resale price.

| ID | Project / layout | Price | Rent | Fee | Other/month | Entry cash | Gross % | Standard/month | Full year | Nominal 5y exit | 8% 5y exit |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R237 | Evo SOHO Suite; 454sf | 248,000 | 1,300 | 230 | 160 | 52,200 | 6.29 | 82 | -2,239 | 278,764 | 306,802 |
| R238 | D'Cerrum; 949sf | 250,000 | 1,000 | 220 | 160 | 52,500 | 4.80 | -216 | -5,515 | 297,679 | 329,438 |
| R239 | Dwiputra Residences; 950sf | 520,000 | 2,300 | 300 | 220 | 103,000 | 5.31 | -72 | -5,806 | 583,581 | 640,388 |
| R240 | Geo Bukit Rimau; 875sf | 500,000 | 1,900 | 280 | 200 | 100,000 | 4.56 | -372 | -8,770 | 578,554 | 637,116 |
| R241 | Habitus Denai Alam; 685sf | 390,000 | 1,650 | 260 | 180 | 73,500 | 5.08 | -164 | -5,780 | 441,165 | 483,524 |
| R242 | GAIA Residences; 660sf | 380,000 | 1,500 | 230 | 180 | 77,000 | 4.74 | -244 | -6,591 | 440,353 | 485,274 |
| R247 | The Parque Residences; 731sf | 470,000 | 1,500 | 300 | 180 | 90,500 | 3.83 | -673 | -11,735 | 558,231 | 615,404 |
| R248 | Alanis Residence; 550sf | 210,000 | 1,200 | 200 | 160 | 51,500 | 6.86 | 163 | -1,162 | 239,791 | 266,269 |
| KV14 | Solstice @ Pan'gaea; 450sf | 200,000 | 1,200 | 180 | 150 | 45,000 | 7.20 | 223 | -324 | 220,164 | 242,565 |
| R351 | MKH Boulevard II; 550sf | 270,000 | 1,500 | 200 | 160 | 65,500 | 6.67 | 224 | -731 | 303,634 | 336,474 |
| R352 | Ascotte Boulevard; 860sf | 218,000 | 900 | 220 | 160 | 47,700 | 4.95 | -189 | -5,085 | 262,977 | 291,912 |
| R353 | The Arc; 913sf | 220,000 | 1,500 | 250 | 180 | 58,000 | 8.18 | 373 | 820 | 244,881 | 272,368 |
| R354 | Shaftsbury Putrajaya; 686sf | 368,000 | 1,800 | 300 | 180 | 70,200 | 5.87 | 34 | -3,558 | 407,378 | 445,702 |
| R355 | Alanis Residence compact; 450sf | 249,000 | 1,200 | 180 | 150 | 57,350 | 5.78 | 28 | -2,667 | 287,139 | 318,122 |
| R356 | Aman 1 Tropicana Urban Homes; 870sf | 338,000 | 1,500 | 250 | 180 | 75,700 | 5.33 | -97 | -4,823 | 393,756 | 436,081 |
| R357 | Habitus Denai Alam original compact control; 565sf | 360,000 | 1,300 | 350 | 170 | 74,000 | 4.33 | -485 | -9,155 | 433,264 | 479,540 |
| R358 | GAIA Residences larger family control; 750sf | 500,000 | 1,700 | 280 | 180 | 90,000 | 4.08 | -572 | -10,730 | 578,348 | 634,206 |
| R359 | Alanis Residence family control; 807sf | 365,000 | 1,600 | 280 | 180 | 79,750 | 5.26 | -135 | -5,374 | 424,006 | 468,926 |
| R360 | Savanna Executive Suites family; 956sf | 350,000 | 1,500 | 260 | 180 | 67,500 | 5.14 | -155 | -5,517 | 399,205 | 438,334 |
| R361 | Amber Residences compact two-bedroom; 657sf | 430,000 | 1,700 | 240 | 180 | 89,500 | 4.74 | -254 | -6,902 | 497,868 | 549,228 |

Seven inputs meet the simplified monthly rule; five meet 6% gross; only R353 is annually nonnegative. These are arithmetic counts, not verified opportunities. R353's RM820 annual buffer is smaller than the RM1,200 annual unquoted-cost sensitivity alone. None has a validated clearing interval or current ordinary lease/finance approval.

## Rent and acquisition constraints

Holding proxies fixed, monthly coverage uses rent >= instalment + fee. Annual neutrality uses 11 × rent >= 12 × (instalment + fee + other). These are income constraints, not fair values, recommended bids or validated margins of safety.

| ID | Rent for standard | Rent for 6% gross | Rent for annual neutrality | Price at annual neutrality |
|---|---:|---:|---:|---:|
| R237 | 1,218 | 1,240 | 1,504 | 201,172 |
| R238 | 1,216 | 1,250 | 1,501 | 134,673 |
| R239 | 2,372 | 2,600 | 2,828 | 398,581 |
| R240 | 2,272 | 2,500 | 2,697 | 316,606 |
| R241 | 1,814 | 1,950 | 2,175 | 269,136 |
| R242 | 1,744 | 1,900 | 2,099 | 242,160 |
| R247 | 2,173 | 2,350 | 2,567 | 224,594 |
| R248 | 1,037 | 1,050 | 1,306 | 185,698 |
| KV14 | 977 | 1,000 | 1,229 | 193,226 |
| R351 | 1,276 | 1,350 | 1,566 | 254,707 |
| R352 | 1,089 | 1,090 | 1,362 | 111,670 |
| R353 | 1,127 | 1,100 | 1,425 | 237,141 |
| R354 | 1,766 | 1,840 | 2,123 | 293,603 |
| R355 | 1,172 | 1,245 | 1,442 | 193,226 |
| R356 | 1,597 | 1,690 | 1,938 | 237,141 |
| R357 | 1,785 | 1,800 | 2,132 | 168,550 |
| R358 | 2,272 | 2,500 | 2,675 | 275,619 |
| R359 | 1,735 | 1,825 | 2,089 | 252,616 |
| R360 | 1,655 | 1,750 | 2,002 | 234,631 |
| R361 | 1,954 | 2,150 | 2,327 | 285,656 |

Entry cash = 15% of purchase price + fit-out allowance: 10% equity and 5% acquisition-cost allowance. The allowance is not a tax/legal quotation or waiver confirmation. Exit proceeds allow 3% selling cost. Results are pre-tax; actual tax, legal, consent, insurance, repairs, assessment, service obligations and financing costs can differ. The separate RM1,200/year + RM5,000 exit buffer tests omitted costs; it does not certify completeness.

## New branches and the counterexample

| Parent | Branch | Standard/month | Full first year | Entry cash | Nominal exit | 8% exit |
|---|---|---:|---:|---:|---:|---:|
| R360 | restricted_Bumi330k_control | -75 | -4,560 | 64,500 | 373,972 | 410,586 |
| R360 | FF2300_extra25k | 645 | 3,283 | 92,500 | 379,617 | 421,235 |
| R360 | quarantined_auction310k | 5 | -3,604 | 61,500 | 348,739 | 382,838 |
| R360 | initial_vacancy3 | -155 | -8,517 | 67,500 | 402,297 | 442,806 |
| R361 | extra_bay100 | -254 | -8,102 | 89,500 | 504,054 | 556,748 |
| R361 | fee_up50 | -304 | -7,502 | 89,500 | 500,961 | 552,988 |

R360's RM1,500 base rent is a dated whole-unit index scenario with unverified fit-out matching. Its RM2,300 control is an actual FF asking advertisement for another two-bay unit; the costed branch raises total fit-out from RM15k to RM40k. That branch has positive annual carry, but its flat-price five-year equity result remains approximately -RM28,728. Neither family utility nor 7.89% conditional gross yield independently proves a sound entry. The lower Bumi and auction branches remain quarantined despite arithmetic improvements.

R361 uses a one-bay PF sale versus a two-bay FF rent. Additional bay cost is a hypothetical sensitivity, not proof a bay can be rented. Even the favourable base does not meet the standard. Its 1500/1900 low/high rent cells are sensitivities, not distinct verified leases.

## Forward supply without fabricated rent

Kanopi B08-T01 retains null rent. At the developer headline RM590,888, standard coverage needs RM2,705, 6% gross RM2,954 and stabilised annual neutrality RM3,191. At the ordinary brochure RM675,888, the requirements become RM3,043 / RM3,379 / RM3,560. These use RM350 fee and RM220 other monthly proxies. No progressive interest, construction-period yield, incentive eligibility or future tenant allocation is asserted.

Other future supply in the regional synthesis is not assigned operating cashflows. Riang's compact/affordable cohort, M Sinar's affordable/ordinary split and Perdana Park's future phase cannot borrow rents or eligibility from an existing component.

## Stress and future buyer funding

All cases are evaluated at: 5.5% interest; 20% rent reduction; 20% fee increase; first twelve months without rent; RM30k works in month24; lender value 15% below purchase; 25-year term; twelve-month sale delay; extra annual/exit cost; low/high rent; and combined stress. Combined five-year stress uses 5.5%, 80% rent, 120% fee, six paid months in year1 and RM30k works at month1. The joint first-year cash test has no sale.

Valuation/term changes can move debt, initial cash and discounted exits differently; no universal monotonic claim is made for every metric. No-sale resilience is finite and does not prove perpetual holding capacity.

| ID | Combined first-year cash | Combined 5y nominal exit | Future buyer cash at base nominal exit: 90% finance + costs | Diagnostic 70% finance + costs |
|---|---:|---:|---:|---:|
| R237 | -43,375 | 349,877 | 56,815 | 112,567 |
| R238 | -44,787 | 364,168 | 59,652 | 119,188 |
| R239 | -56,079 | 689,928 | 112,537 | 229,253 |
| R240 | -56,311 | 677,078 | 111,783 | 227,494 |
| R241 | -50,603 | 527,930 | 81,175 | 169,408 |
| R242 | -50,311 | 523,732 | 86,053 | 174,124 |
| R247 | -56,539 | 648,731 | 103,735 | 215,381 |
| R248 | -41,220 | 306,345 | 55,969 | 103,927 |
| KV14 | -40,232 | 285,775 | 48,025 | 92,057 |
| R351 | -43,259 | 378,997 | 70,545 | 131,272 |
| R352 | -43,412 | 325,695 | 54,447 | 107,042 |
| R353 | -41,320 | 317,388 | 61,732 | 110,709 |
| R354 | -49,183 | 495,429 | 76,107 | 157,582 |
| R355 | -43,073 | 356,156 | 63,071 | 120,499 |
| R356 | -48,163 | 474,463 | 84,063 | 162,814 |
| R357 | -51,719 | 513,645 | 84,990 | 171,643 |
| R358 | -57,031 | 673,779 | 101,752 | 217,422 |
| R359 | -49,681 | 508,507 | 88,601 | 173,402 |
| R360 | -49,003 | 480,870 | 74,881 | 154,722 |
| R361 | -52,395 | 587,939 | 99,680 | 199,254 |

The 70% future-finance diagnostic is a stress assumption, not a change to the 90% baseline or a legal loan cap. Future investor values at 5/6/7% operating yields are in the results file. Those yields are scenarios, not market cap rates; owner buyers also need evidence of willingness and ability to pay. A nominal break-even price only states what the seller would require.

## Rank sensitivity and portfolio boundary

Fifteen selected pairs generate 135 independent low/base/high rent combinations. Annual-cash leadership reverses in thirteen pairs. R353 remains ahead of R354 within this particular grid; R241 remains ahead of R357. That does not clear either case's source/rights/cost holds.

All 190 synthetic pairs preserve RM150k protected reserves under RM500k starting cash in the specific combined first-year test. The assumed capital is not the user's balance sheet. Same-project alternatives R248/R355/R359, R241/R357 and R242/R358 cannot be counted as independent allocation opportunities; neither can a parent and its branch. Common tenant, transport, credit, developer-package and management risks remain correlated. Whole-programme allocation is a later task, not completed by these pair paths.

## Interpretation

A current shortfall places an expression at lowest ordinary-income research priority. A transition thesis may still be studied, but requires a falsifiable rent mechanism, timing, total funded carry and an adverse exit. No base rent is increased merely because a catalyst is plausible. The full-cost results support continued evidence verification, not a purchase recommendation.
