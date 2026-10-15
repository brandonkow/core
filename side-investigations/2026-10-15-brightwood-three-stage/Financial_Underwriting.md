# Brightwood — financial and terminal underwriting

Date:15October2026. All amounts MYR. These are reproducible scenarios, not verified forecasts or a lender quotation. [Inputs](Financial_Inputs.json), [results](Financial_Results.json), [model](financial_model.py).

## Price and debt basis

The user's latest instruction overrides the provisional nett-loan assumption for this case: loan =90% of gross price;4%;35years. Gross yield =12 × assumed monthly rent / nett consideration. Do not call the loan90% of nett.

D: gross551,000; rounded nett lead495,000; loan495,900. B:555,000;499,000;499,500. The slight loan-over-nett differences reflect approximate quoted inputs and package rounding; no cashback is assumed available. The model credits at most the nett acquisition price against purchase funding while carrying the full gross-based debt. D900 and B500 excess proceeds are uncredited, not invented spendable cash or rent.

No exact unit, rebate-payment schedule or bank offer was supplied. A later loan of90% of nett would be a different sensitivity, not this base. A lower bank valuation is separately tested at90% of85% of gross.

## Operating assumptions

- Fee proxy:0.35 × main BUA per month, including sinking contribution per S02. Actual management-only comparison is unresolved. No fee decrease is assumed. PES share-unit allocation may raise variant charges.
- Eleven paid months per stream/year;5% of collected rent for ordinary repairs/replacement; letting provision0.5 month of each stream's rent per year, summed once; other recurring allowance200/month per parcel for rates/insurance and unquoted owner costs. Tenant utilities excluded unless owner-paid; a100/month increment is tested.
- D is two1,300 streams in the working case, with only one bay across both. Parking is not rented twice. Asymmetric10/8paid months and one side earning zero for the entire hold are separate failures.
- Fit-out allowances: D40k, B30k, C40k, A45k. They are planning allowances, not contractor quotes. No unsupported developer-furnishing savings or resale recovery is booked.
-5% of gross acquisition-cost allowance and3% disposal allowance. These are unquoted buffers, not tax/legal-fee calculations. Returns are pre-tax. Exact tax, legal, consent, financing-insurance and other costs are not authenticated; no exemption is assumed. Zero acquisition-cost diagnostic and extra10k exit cost test sensitivity.
- No rent growth, fee-stability guarantee, capital appreciation, rental guarantee, subsidy, lease renewal or unearned catalyst uplift in the working base.

## Working cases at starting prices

| Type | Nett lead | Gross | Loan | Assumed rent | Gross yield/nett | Monthly loan | Fee proxy | Simplified monthly surplus | Annual cash after modelled operating costs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| D | 495,000 | 551,000 | 495,900 | 2,600 | 6.30% | 2,196 | 251 | +154 | −5,886 |
| B | 499,000 | 555,000 | 499,500 | 2,300 | 5.53% | 2,212 | 258 | −169 | −9,146 |
| C | 622,000 | 692,000 | 622,800 | 2,600 | 5.02% | 2,758 | 335 | −492 | −13,636 |
| A | 665,000 | 739,000 | 665,100 | 2,800 | 5.05% | 2,945 | 379 | −524 | −14,423 |

D passes simplified monthly coverage at2,600; A/B/C working cases are current shortfalls and therefore lowest ordinary-income research priority, not universal Reject. B can pass the simple comparison around2,470 but still require much more rent for full annual cash neutrality. None of the working cases is annual-positive.

Annual cash for equal11paid-month assumptions is:

`9.95 × total monthly rent − 12 × (loan instalment + combined fee + other allowance)`

because `11 × 95% − 0.5 = 9.95`. Annual-neutral rent is the fixed annual burden divided by9.95. This is a cashflow test including principal repayment, distinct from operating NOI or economic profit.

| Type | Rent for preferred6%gross/nett | Rent to cover loan + fee monthly | Rent for annual cash neutrality |
|---|---:|---:|---:|
| D | 2,475 | 2,446 | 3,192 |
| B | 2,495 | 2,469 | 3,219 |
| C | 3,110 | 3,092 | 3,970 |
| A | 3,325 | 3,324 | 4,250 |

## D upside must be tested, not dismissed

| Total D rent | Per-side equal split | Annual cash | Nominal exit needed after48-month build +60-month operation |
|---|---:|---:|---:|
| 2,200 | 1,100 | −9,866 | 635,535 |
| 2,600 | 1,300 | −5,886 | 615,020 |
| 3,000 | 1,500 | −1,906 | 594,505 |
| 3,200 | 1,600 | +84 | 584,247 |

At3,200, annual surplus is only84: a small fee increase, bill inclusion or turnover defeats it. Two rents near1,600 are conceivable, but today's asking choices S03–S05 do not establish equivalent space/privacy or future collections. This is the most decision-sensitive empirical question. A higher confirmed rent would improve the case; the framework does not deny it merely because the working scenario is negative.

## D versus B ranking reversal

D's research preference is not a robust return ranking. If both collect2,600, D's annual carry is approximately−5,886 versus B−6,161, only275/year better. Yet B's lower assumed fit-out produces a lower nominal recovery price,610,075 versus D615,020. With D2,200 and B2,600, B also wins annual carry (−6,161 versus−9,866). These rows already exist in the tested rent scenarios.

D therefore needs a real, sustained two-suite income advantage to justify its extra fit-out and narrower ordinary-family fallback. B with two usable bays and equivalent collected rent could be the stronger overall alternative. No unsupported rent difference is used as conclusive ranking evidence.

## Every type and price endpoint

PES variants have no authenticated nett starting offer, so do not manufacture yield. Fees below use main BUA only, provisionally; a share-unit or PES-inclusive bill could be higher.

| Type | Gross price | Loan instalment | Loan + fee coverage rent | Annual-neutral rent |
|---|---:|---:|---:|---:|
| A | 739,000 | 2,945 | 3,324 | 4,250 |
| A | 843,960 | 3,363 | 3,742 | 4,754 |
| A(A) | 853,000 | 3,399 | 3,778 | 4,797 |
| A(A) | 927,150 | 3,695 | 4,073 | 5,154 |
| B | 555,000 | 2,212 | 2,469 | 3,219 |
| B | 661,125 | 2,635 | 2,892 | 3,729 |
| C | 692,000 | 2,758 | 3,092 | 3,970 |
| C | 745,680 | 2,972 | 3,306 | 4,228 |
| C(A) | 812,000 | 3,236 | 3,570 | 4,547 |
| C(A) | 822,000 | 3,276 | 3,610 | 4,595 |
| D | 551,000 | 2,196 | 2,446 | 3,192 |
| D | 620,550 | 2,473 | 2,723 | 3,526 |
| D(A) | 630,000 | 2,511 | 2,761 | 3,571 |
| D(A) | 643,160 | 2,563 | 2,814 | 3,634 |

The extra bay/PES must earn a real utility or rent/exit benefit; apparent low PSF using outdoor area as equivalent enclosed space is not value evidence.

## Construction, delayed income and cash funding

The base is48months without rent, followed by60operating months:108months from acquisition, not a five-year acquisition-to-exit claim. Construction interest uses a linear progressive draw with monthly midpoint utilisation averaging50% of the gross-based loan. It is not48months of full instalments. Interest-only construction and a fresh35-year amortisation period at full draw are modelling conventions;31-year and25-year repayment scenarios test shorter actual availability. No lender has approved39total years.

Fit-out cash is reserved at delivery; fees start with operation. Acquisition allowance is reserved upfront. Actual progress bills, developer completion, bank disbursements and rebate dates may differ. Front/back-loaded draw and36/60month construction are separate tests.

| Type | Entry/fit-out cash excluding construction interest | Construction interest | Five-year operating cash | Peak cumulative cash required before sale | Remaining debt | Nominal break-even sale | Flat-nett-price total profit |
|---|---:|---:|---:|---:|---:|---:|---:|
| D | 67,550 | 39,672 | −29,429 | 136,651 | 459,918 | 615,020 | −116,419 |
| B | 57,750 | 39,960 | −45,731 | 143,441 | 463,257 | 625,461 | −122,668 |
| C | 74,600 | 49,824 | −68,182 | 192,606 | 577,611 | 794,038 | −166,877 |
| A | 81,950 | 53,208 | −72,116 | 207,274 | 616,841 | 849,603 | −179,065 |

Peak cash is a model funding envelope, not a single upfront invoice. It excludes a separately reserved rebate-timing bridge: a10%gross deposit could require D55,100 or B55,500 temporarily. Adding it to the full-period peak gives a conservative reserve envelope, not an accurately timed settlement cashflow; exact timing is unknown. No low-deposit promotion eliminates works, interest, vacancies or full loan liability.

D's615,020 exit is24.25% above nett495k over nine modelled years (about2.44% annualised price growth burden). It is not a price forecast. Its required growth remains positive even at stronger rent. At the working rent and even a diagnostic zero acquisition-cost allowance, D still needs about586,618 to recover nominal costs. The decision is therefore not caused solely by the5% buffer.

No principal double-count: terminal recovery equals total equity/cost/construction cash paid minus operating cashflow plus remaining debt, divided by97%. An independent purchase-plus-interest-plus-cost-minus-collected-rent identity is checked. No8% equity hurdle is adopted as the user's requirement; nominal break-even is already a low bar, excluding opportunity cost and inflation.

## D sensitivities

| Scenario | Stabilised annual cash | Peak cumulative cash before sale | Nominal break-even exit |
|---|---:|---:|---:|
| rate_5.5 | −11,494 | 179,569 | 668,652 |
| fee_.50 | −7,175 | 143,095 | 621,663 |
| term_31 | −7,475 | 144,595 | 614,160 |
| term_25 | −10,948 | 161,961 | 612,281 |
| valuation_down15 | −1,934 | 184,916 | 593,149 |
| build_36 | −5,886 | 126,733 | 604,795 |
| build_60 | −5,886 | 146,569 | 625,245 |
| draw_frontloaded | −5,886 | 156,513 | 635,496 |
| draw_backloaded | −5,886 | 116,811 | 594,566 |
| extra_operating100 | −7,086 | 142,651 | 621,206 |
| works30k | −5,886 | 166,651 | 645,948 |
| fitout_extra20k | −5,886 | 156,651 | 635,639 |
| extra_exit10k | −5,886 | 136,651 | 625,329 |
| acquisition_allowance_zero_diagnostic | −5,886 | 109,101 | 586,618 |
| exit_delay12 | −5,886 | 142,537 | 612,738 |
| no_rent_first12 | −5,886 | 163,821 | 643,030 |
| correlated_shock | −15,558 | 332,222 | 739,227 |
| asymmetric_10_8_months | −10,826 | 161,351 | 640,484 |
| one_side_zero_entire_hold | −18,821 | 201,326 | 681,695 |
| gross_paid_no_rebate_counterfactual | −5,886 | 191,751 | 671,824 |
| rounded_net_plus_delta | −5,886 | 136,651 | 615,020 |

Stabilised annual cash excludes one-off works and initial-year void shock; first-year cash is separately stored. A shorter term increases cash drain but can reduce total interest, so a lower required terminal price is not proof of improved affordability. Lower valuation likewise requires more initial equity despite a smaller loan. A delayed exit may reduce remaining debt enough to lower nominal break-even while still consuming more cash and time.

The correlated shock applies5.5%,31-year amortisation,60-month build,72-month operation,20%lower rent, six paid months in year1,0.50psf fee,300/month other costs,30k works and15%lower valuation simultaneously. It is not a worst-case bound. D's first operating year is roughly−55,438 and cumulative funding332,222 before sale. Contractor default/abandonment or inability to finance completion can be worse and are not assigned invented probabilities.

## Entry-price thresholds and financing dependence

| D assumed total rent | Annual-neutral maximum gross | Equivalent nett if current package ratio stays | Nett cap for6%gross yield |
|---|---:|---:|---:|
| 2,200 | 344,687 | 309,655 | 440,000 |
| 2,300 | 365,494 | 328,348 | 460,000 |
| 2,600 | 427,916 | 384,425 | 520,000 |
| 2,800 | 469,531 | 421,811 | 560,000 |
| 3,000 | 511,145 | 459,196 | 600,000 |
| 3,200 | 552,760 | 496,581 | 640,000 |

These roots are scenario constraints, not fair values or bids. **A further nett-only rebate with gross and the90%gross loan unchanged does not reduce the instalment or cure operating shortfall.** Lower gross/debt, independently funded principal reduction, demonstrably higher collected rent or genuine cost reduction must change the annual equation. No principal-reduction funding is assumed.

## Exit buyer and opportunity cost

At D's615,020 required exit, a6%gross-yield investor needs roughly3,075 monthly rent; our working rent is2,600. The new buyer's standard90%/4%/35 payment would be2,451, before fees and other costs;80%/5.5%/25stress payment is3,021 and requires more equity. Neither a target yield nor calculator payment proves that buyer's willingness or funding. No unsupported owner-occupier premium rescues the exit.

Gross-yield price at2,600/6% is520k before other adjustments. This is an investor-yield diagnostic, **not a validated market ceiling**. The contrast with615k cost recovery exposes the exit burden. B/A/C household channels also need actual budgets and substitutes, not a guaranteed floor.

S10/S11 challenge waiting for a new build at similar acquisition quantum, but their own fee, condition, lease and governance are unverified. No alternate purchase is recommended merely because a ready unit can collect rent sooner.

## Portfolio test

Synthetic cash500k and protected reserve150k are inherited analytical controls, not user finances. Holding one D and one B combines the same developer, completion, building, service system and local demand: two suites/two units do not provide corresponding independent diversification.

Under the synchronized correlated shock, minimum synthetic cash is-171,149, failing the protected reserve. Starting cash of about821,149 would be needed to retain150k before a separate rebate bridge. The pair is not recommended. Actual credit utilisation, income, existing debt, commitments and liquid reserves remain unknown; G8 cannot clear.

## Verification

53financial evaluations,14type/price screens,12annual-neutral roots and45payment parity checks against the frozen engine passed. Amortisation recurrence, closed-form debt, principal conservation and two independent terminal recovery identities agree. These tests verify scenario arithmetic, not rent, price, developer delivery or market outcomes.
