# Cheras - approved baseline calibration bridge

Date: 6 October 2026. Applies the user-approved 90% LTV / 4% / 35-year rent-coverage convention and preferred 6% gross yield to the original nine case inputs. This is a subsequent calibration, not a revision of earlier evidence or a completed new underwriting.

## Evidence and comparison boundary

Price, rent and costs are carried from [the original financial workpaper](Cheras_Financial_Underwriting.md). Prices are historical selected asks; rent and costs remain assumptions. No fresh availability, achieved rent, fee invoice or normalised G0 price is established. The old fee allowance covers estimated service/sinking charges and is used as a disclosed proxy here. It cannot certify a management-only break-even result. Exact fee inclusion and actual bank terms remain unverified.

The user subsequently fixed 90% LTV for every future baseline comparison. Standard principal is 90% of acquisition price; 80% is retained only as a historical sensitivity. Actual lender margin or valuation constraints must be separately tested and cannot be used to relabel the standard result. Personal income is not used to make a failed property screen pass.

Standard definition: monthly rent minus full mortgage instalment at 4%/35 years minus management fee. The following calculations substitute the disclosed fee proxy. Gross yield uses twelve monthly rents divided by the selected ask; 6% is a preference, not a hard gate. Complete-cost scenarios remain separate and still exclude tax, transaction-specific expenses and unexpected large works as described in the original workpaper.

## Standard monthly coverage scenarios

| Case | Rent assumed | Fee proxy | 90% standard instalment | 90% standard monthly balance | 80% historical monthly balance | Gross yield | 6% target reached? |
|---|---:|---:|---:|---:|---:|---:|---|
| C01 M Vertica | 2,400 | 350 | 1,949 | +101 | +318 | 5.89% | Below preference |
| C02 Shamelin Star | 2,600 | 400 | 2,789 | -589 | -280 | 4.46% | Below preference |
| C03 EkoCheras duplex | 2,300 | 350 | 2,072 | -122 | +108 | 5.31% | Below preference |
| C04 Aster Type B | 2,400 | 350 | 2,152 | -102 | +137 | 5.33% | Below preference |
| C05 Maxim Residences | 2,400 | 350 | 1,913 | +137 | +350 | 6.00% | Yes, scenario |
| C06 Riana South | 2,700 | 400 | 2,371 | -71 | +192 | 5.45% | Below preference |
| C07 Green Residence | 2,000 | 400 | 2,152 | -552 | -313 | 4.44% | Below preference |
| C08 Windows on the Park large | 3,500 | 850 | 3,586 | -936 | -538 | 4.67% | Below preference |
| C09 Scot Pine | 2,200 | 450 | 1,985 | -235 | -14 | 5.30% | Below preference |

A positive figure is a pass only within these assumed-input/proxy scenarios. Unknown actual rent/management fee remains unknown. No case is upgraded to Deploy.

## Separate complete-cost holding view

This retains eleven paid rental months and the original other-cost allowance, in addition to the fee proxy and the new 35-year mortgage. It is not the definition of the user's standard monthly shortfall.

| Case | Annual cashflow at standard 90% LTV | Annual cashflow at historical 80% LTV | Monthly rent needed at standard 90%, eleven paid months |
|---|---:|---:|---:|
| C01 | -2,984 | -386 | 2,671 |
| C02 | -11,474 | -7,754 | 3,643 |
| C03 | -5,566 | -2,803 | 2,806 |
| C04 | -5,423 | -2,553 | 2,893 |
| C05 | -2,553 | -3 | 2,632 |
| C06 | -5,353 | -2,191 | 3,187 |
| C07 | -10,423 | -7,553 | 2,948 |
| C08 | -17,138 | -12,356 | 5,058 |
| C09 | -7,414 | -4,768 | 2,874 |

## Decision consequence

Under the approved 90% LTV standard, 2 of nine expressions cover the fee proxy: C01, C05. The historical 80% sensitivity covers 5: C01, C03, C04, C05, C06. These are not verified tenancies or lending decisions.

The previous statement that all nine have negative annual cashflow referred to the original 30-year, eleven-paid-month, broader-cost model. It must not be restated as all nine failing the newly defined standard monthly coverage test. The two measures answer different questions.

Maxim remains the provisional single-choice investigation preference from the subsequent conversation; this bridge does not prove management, buyer adoption, matched clearing or superiority over unresearched two-bedroom alternatives. All original gate stops remain. No ranking is promoted solely because a longer term reduces instalments.

The original 30-year exit prices, five-year debt balances, return hurdles and portfolio stresses remain historical scenario results. This bridge does not relabel them as 35-year results. A later executable underwriting must recalculate those quantities, all relevant costs and actual financing before any Deploy decision.

## Verification

Mortgage amounts were reconciled to a 420-month principal recurrence; complete-cost cashflow was independently reconciled to standard monthly coverage less the unpaid month and annual other costs. Original model/report/result files are not modified. The earlier bridge/code/results are retained in `baseline-history/pre-90pct/` as historical records. Source and approval provenance: [approved SOP](../sop/Approved_Execution_Supplement.md) and [approval register](../sop/Founder_QA_Approval_Register.md).
