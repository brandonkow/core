# Phase 7 Batch 02 - Financial and switching tests

As of 6 October 2026. Currency MYR. All results are conditional scenarios, not personal financial advice, bank quotes or valuations. No investment return target was supplied; nominal break-even is a diagnostic, not an adequate investment hurdle.

## Locked mandate and inputs

RM500,000 cash including RM150,000 protected reserve; RM20,000 gross monthly household income; RM4,000 existing debt. 80% LTV, 30 years, 4% base and 5.5% stress. Five-year hold; no rent growth; eleven rent-paying months per base year. Entry costs 5% of price plus refurbishment; exit costs 3%. Generic allowances, not statutory quotations. Income/disposal tax, loan lock-in costs, equity opportunity cost and household expenses are excluded. Household reserve adequacy is unverified.

| ID | Expression | Price | Rent/month | Fees / other per month | Refurb | Extra liabilities |
|---|---|---:|---:|---:|---:|---:|
| K1 | Kiara original one bay | 850,000 | 3,200 | 520 / 150 | 50,000 | 0 |
| A1 | Aster original C | 685,000 | 2,800 | 400 / 150 | 20,000 | 0 |
| S1 | Sterling two bays | 608,000 | 2,500 | 350 / 150 | 40,000 | 0 |
| V1 | Venice Hill Tower 10 | 280,000 | 1,400 | 350 / 150 | 40,000 | 0 |
| K2 | Kiara two-bay high-floor ask | 1,350,000 | 3,500 | 520 / 150 | 50,000 | 0 |
| KA | Kiara past auction plus liability scenario | 558,000 | 3,200 | 520 / 150 | 50,000 | 200,000 |
| A2 | Aster C low-floor west-facing ask | 650,000 | 2,800 | 400 / 150 | 20,000 | 0 |
| AB | Aster B 810 sf ask | 540,000 | 2,400 | 350 / 150 | 20,000 | 0 |
| AD | Aster duplex asking scenario | 750,000 | 2,800 | 450 / 150 | 20,000 | 0 |

K1/A1 retain Batch 01 inputs. K2/KA are comparisons, not substitutes silently replacing K1. KA is a PAST reserve plus a RM200,000 liability assumption drawn from an unverified agent warning of RM200,000-plus; actual debt allocation and auction outcome remain unknown. That liability is extra to generic transaction costs and the future levy. A2 is a separate advertisement, not a proven price reduction of A1. AD uses a dated asking example, not an available verified unit. Source IDs and dates are in the evidence log.

S1 rent RM2,500 is assumed between imperfect one-bay partial/full and three-bay furnished asking comparators; no automatic parking premium. S1 RM350 fees replaces the stale RM0.18 psf advertising claim with an allowance, informed by a different-unit RM344 claim. V1 RM1,400 rent is assumed below a larger ground-floor Tower 10 ask of RM1,600; it is not a matched rent. A2 uses A1 rent unchanged to isolate price. AB/AD rents and all refurb/other allowances are assumptions. Fees intend to include sinking contributions; actual invoices are absent.

## Capital survival

Stress: +1.5 percentage-point rate, rent -20%, six months vacancy, twelve months unable to sell and RM30,000 levy simultaneously. The separate zero-rent sensitivity gives no rent for twelve months.

| ID | Entry cash | Mortgage base / stress | Stress burn | Cash left | RM150k reserve | Cash-only price ceiling |
|---|---:|---:|---:|---:|---|---:|
| K1 | 262,500 | 3,246 / 3,861 | 69,012 | 168,488 | Pass | 910,716 |
| A1 | 191,250 | 2,616 / 3,111 | 60,498 | 248,252 | Pass | 1,007,659 |
| S1 | 192,000 | 2,322 / 2,762 | 57,141 | 250,859 | Pass | 939,221 |
| V1 | 110,000 | 1,069 / 1,272 | 44,542 | 345,458 | Pass | 921,881 |
| K2 | 387,500 | 5,156 / 6,132 | 94,825 | 17,675 | Fail | 915,445 |
| KA | 389,500 | 2,131 / 2,535 | 53,095 | 57,405 | Fail | 253,918 |
| A2 | 182,500 | 2,483 / 2,953 | 58,590 | 258,910 | Pass | 1,007,659 |
| AB | 155,000 | 2,062 / 2,453 | 53,914 | 291,086 | Pass | 1,003,324 |
| AD | 207,500 | 2,864 / 3,407 | 64,641 | 227,859 | Pass | 1,005,689 |

A cash-only price ceiling is the solution of entry cash + stress burn = RM350,000 with all other inputs fixed. It is never an entry recommendation or market-value ceiling. Unknown title, management, permanent externalities or valuation can stop a purchase far below it.

## Return and rent hurdles

| ID | Annual base cash flow | Neutral monthly rent | Five-year break-even sale | Required annual price growth | Profit: exit -20% / flat / +15% |
|---|---:|---:|---:|---:|---:|
| K1 | -11,797 | 4,272 | 965,493 | 2.6% | -276,929 / -112,029 / 11,646 |
| A1 | -7,195 | 3,454 | 745,234 | 1.7% | -191,317 / -58,427 / 41,241 |
| S1 | -6,366 | 3,079 | 684,294 | 2.4% | -191,958 / -74,006 / 14,458 |
| V1 | -3,433 | 1,712 | 339,966 | 4.0% | -112,487 / -58,167 / -17,427 |
| K2 | -31,413 | 6,356 | 1,568,452 | 3.0% | -473,798 / -211,898 / -15,473 |
| KA | 1,586 | 3,056 | 809,617 | 7.7% | -352,321 / -244,069 / -162,880 |
| A2 | -5,591 | 3,308 | 701,836 | 1.5% | -176,381 / -50,281 / 44,294 |
| AB | -4,349 | 2,795 | 585,030 | 1.6% | -148,439 / -43,679 / 34,891 |
| AD | -10,774 | 3,779 | 828,922 | 2.0% | -222,055 / -76,555 / 32,570 |

No exit price is forecast. These amounts distinguish capital survival from return sufficiency. KA losses include the assumed inherited liability; its growth hurdle is relative to the reserve, which is not total acquisition basis. The one-year shock and five-year base return are separate scenarios, not double-counted.

## Financing and levy sensitivity

| ID | Scenario | Entry cash | Cash after shock | Reserve |
|---|---|---:|---:|---|
| K1 | 70% LTV | 347,500 | 89,280 | Fail |
| K1 | 90% LTV | 177,500 | 247,697 | Pass |
| K1 | Valuation -15% | 364,500 | 73,438 | Fail |
| K1 | RM50k levy | 262,500 | 148,488 | Fail |
| A1 | 70% LTV | 259,750 | 184,419 | Pass |
| A1 | 90% LTV | 122,750 | 312,085 | Pass |
| A1 | Valuation -15% | 273,450 | 171,653 | Pass |
| A1 | RM50k levy | 191,250 | 228,252 | Pass |
| S1 | 70% LTV | 252,800 | 194,202 | Pass |
| S1 | 90% LTV | 131,200 | 307,517 | Pass |
| S1 | Valuation -15% | 264,960 | 182,870 | Pass |
| S1 | RM50k levy | 192,000 | 230,859 | Pass |
| V1 | 70% LTV | 138,000 | 319,366 | Pass |
| V1 | 90% LTV | 82,000 | 371,550 | Pass |
| V1 | Valuation -15% | 143,600 | 314,147 | Pass |
| V1 | RM50k levy | 110,000 | 325,458 | Pass |
| K2 | 70% LTV | 522,500 | -108,127 | Fail |
| K2 | 90% LTV | 252,500 | 143,476 | Fail |
| K2 | Valuation -15% | 549,500 | -133,288 | Fail |
| K2 | RM50k levy | 387,500 | -2,325 | Fail |
| KA | 70% LTV | 445,300 | 5,407 | Fail |
| KA | 90% LTV | 333,700 | 109,403 | Fail |
| KA | Valuation -15% | 456,460 | -4,993 | Fail |
| KA | RM50k levy | 389,500 | 37,405 | Fail |
| A2 | 70% LTV | 247,500 | 198,339 | Pass |
| A2 | 90% LTV | 117,500 | 319,481 | Pass |
| A2 | Valuation -15% | 260,500 | 186,224 | Pass |
| A2 | RM50k levy | 182,500 | 238,910 | Pass |
| AB | 70% LTV | 209,000 | 240,765 | Pass |
| AB | 90% LTV | 101,000 | 341,407 | Pass |
| AB | Valuation -15% | 219,800 | 230,701 | Pass |
| AB | RM50k levy | 155,000 | 271,086 | Pass |
| AD | 70% LTV | 282,500 | 157,969 | Pass |
| AD | 90% LTV | 132,500 | 297,749 | Pass |
| AD | Valuation -15% | 297,500 | 143,991 | Fail |
| AD | RM50k levy | 207,500 | 207,859 | Pass |

## Portfolio pairs: original expressions plus two new candidates

| Pair | Cash after both entries and shocks | Reserve | Gross-income stress debt proxy |
|---|---:|---|---:|
| K1 + A1 | -83,259 | Fail | 54.9% |
| K1 + S1 | -80,652 | Fail | 53.1% |
| K1 + V1 | 13,946 | Fail | 45.7% |
| A1 + S1 | -889 | Fail | 49.4% |
| A1 + V1 | 93,710 | Fail | 41.9% |
| S1 + V1 | 96,317 | Fail | 40.2% |

A pair passing this cash calculation is not portfolio approval. Cross-market assets share credit/rent risks; two Cheras assets additionally share corridor exposure. Existing assets and liabilities beyond the synthetic debt input are unknown. No correlation coefficient is fabricated.

## Marginal future buyer

No remaining lease is inferred from completion dates. Sterling and Aster require title expiry and lender terms. The following are sensitivity assumptions for ALL cases, not predictions that lenders will impose them.

| ID | 80% LTV / 25 yr / 5.5% payment | 70% LTV / 20 yr / 5.5% payment | Down payment at 70%, before costs | Zero-rent annual shock |
|---|---:|---:|---:|---:|
| K1 | 4,176 | 4,093 | 255,000 | 84,372 |
| A1 | 3,365 | 3,298 | 205,500 | 73,938 |
| S1 | 2,987 | 2,928 | 182,400 | 69,141 |
| V1 | 1,376 | 1,348 | 84,000 | 51,262 |
| K2 | 6,632 | 6,501 | 405,000 | 111,625 |
| KA | 2,741 | 2,687 | 167,400 | 68,455 |
| A2 | 3,193 | 3,130 | 195,000 | 72,030 |
| AB | 2,653 | 2,600 | 162,000 | 65,434 |
| AD | 3,685 | 3,611 | 225,000 | 78,081 |

## Explicit switching arithmetic

At the RM558,000 past reserve, KA can absorb at most RM107,405 of extra cash-paid liabilities before violating the reserve under this stress. This is a scenario threshold, not a legal debt determination.

A1 versus AB: the RM145,000 price difference adds RM554 monthly mortgage, plus the assumed RM50 fee difference. A2 versus AB adds RM420 mortgage plus RM50. The household must value the extra usable space/balcony/bathroom enough to support this premium; that willingness-to-pay is not proven by the floor plan.

S1 versus the RM533,000 conflicting-body Kelana Mahkota ask: RM75,000 adds RM286 monthly mortgage before fee/condition differences. If the RM513,000 header is correct, the gap is RM95,000 and RM363. Verify actual price and bay geometry before selecting the better deal.

Validation: all nine five-year loan balances reconcile to analytic amortisation and all break-even values to a separate purchase/interest/cost/rent identity. Nine base cases, 36 one-factor sensitivities and six joint cases. The model preserves Batch 01 files.
